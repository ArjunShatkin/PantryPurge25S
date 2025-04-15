from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
import json
import traceback
import datetime

recipes = Blueprint('recipes', __name__)
chefs = Blueprint('chefs', __name__)

# ------------------------------------------------------------
# POST /recipes - Create and publish a new recipe

@recipes.route('/recipes', methods=['POST'])
def create_recipe():
    current_app.logger.info('POST /recipes route')

    data = request.json

    recipe_name = data.get('RecipeName')
    chef_id = data.get('ChefID')
    servings = data.get('Servings', 4)
    difficulty = data.get('Difficulty', 'Medium')
    calories = data.get('Calories', 0)
    description = data.get('Description', '')
    cuisine = data.get('Cuisine', 'General')
    prep_time_mins = data.get('PrepTimeMins', 30)
    cook_time_mins = data.get('CookTimeMins', 45)
    publish_date = data.get('PublishDate', '2025-01-01')
    video_url = data.get('VideoUrl','')

    # Required field validation
    if not recipe_name:
        return jsonify({"error": "RecipeName is required."}), 400

    try:
        cursor = db.get_db().cursor()

        query = '''
            INSERT INTO recipes (
                RecipeName, ChefID, Servings, Difficulty, Calories, 
                Description, Cuisine, PrepTimeMins, CookTimeMins, 
                PublishDate, VideoUrl
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING RecipeID;
        '''
        values = (
            recipe_name, servings, difficulty, calories,
            description, cuisine, prep_time_mins, cook_time_mins, publish_date
        )

        cursor.execute(query, values)
        new_id = cursor.fetchone()[0]
        db.get_db().commit()

        return jsonify({
            "message": "Recipe created successfully.",
            "recipe_id": new_id
        }), 201

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500


@recipes.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    current_app.logger.info(f'PUT /recipes/{recipe_id} route')

    data = request.json

    # Extract fields from request
    recipe_name = data.get('RecipeName')
    servings = data.get('Servings')
    difficulty = data.get('Difficulty')
    calories = data.get('Calories')
    description = data.get('Description')
    cuisine = data.get('Cuisine')
    prep_time_mins = data.get('PrepTimeMins')
    cook_time_mins = data.get('CookTimeMins')
    publish_date = data.get('PublishDate')

    # Validate: at least one field must be provided
    if not any([recipe_name, servings, difficulty, calories, description, cuisine, prep_time_mins, cook_time_mins, publish_date]):
        return jsonify({"error": "No fields to update"}), 400

    try:
        cursor = db.get_db().cursor()

        # Dynamically build update query
        fields = []
        values = []

        if recipe_name:
            fields.append("RecipeName = %s")
            values.append(recipe_name)
        if servings is not None:
            fields.append("Servings = %s")
            values.append(servings)
        if difficulty:
            fields.append("Difficulty = %s")
            values.append(difficulty)
        if calories is not None:
            fields.append("Calories = %s")
            values.append(calories)
        if description:
            fields.append("Description = %s")
            values.append(description)
        if cuisine:
            fields.append("Cuisine = %s")
            values.append(cuisine)
        if prep_time_mins is not None:
            fields.append("PrepTimeMins = %s")
            values.append(prep_time_mins)
        if cook_time_mins is not None:
            fields.append("CookTimeMins = %s")
            values.append(cook_time_mins)
        if publish_date:
            fields.append("PublishDate = %s")
            values.append(publish_date)

        values.append(recipe_id)
        query = f"UPDATE recipes SET {', '.join(fields)} WHERE RecipeID = %s"

        cursor.execute(query, tuple(values))
        db.get_db().commit()

        return 'Recipe updated successfully.', 200

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500

# This blueprint will handle routes related to Newsletter submissions
newsletter_routes = Blueprint('newsletter_routes', __name__)

# ------------------------------------------------------------
# /newsletter: Post a recipe to be considered for the newsletter
# ------------------------------------------------------------
# /recipes/<id>/newsletter: Submit a recipe for the newsletter

@recipes.route('/recipes/<int:recipe_id>/newsletter', methods=['POST'])
def submit_recipe_for_newsletter(recipe_id):
    current_app.logger.info(f'POST /recipes/{recipe_id}/newsletter route')

    data = request.get_json()
    current_app.logger.debug(f"Received data: {data}")  # Log incoming data
    
    chef_id = data.get('ChefID')
    
    sub_status = data.get('SubStatus', 'Pending')
    sub_date = datetime.datetime.now()

    if not chef_id:
        return jsonify({"error": "ChefID is required."}), 400

    try:
        cursor = db.get_db().cursor()

        query = '''
            INSERT INTO Newsletter (ChefID, RecipeID, SubStatus, SubDate)
            VALUES (%s, %s, %s, %s);
        '''
        values = (chef_id, recipe_id, sub_status, sub_date)
        cursor.execute(query, values)
        
        sub_id = cursor.lastrowid

        db.get_db().commit()

        return jsonify({
            "message": "Recipe submission to newsletter successful.",
            "SubID": sub_id,
            "ChefID": chef_id,
            "RecipeID": recipe_id,
            "SubStatus": sub_status,
            "SubDate": sub_date.isoformat()
        }), 200

    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Exception: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
        # return jsonify({sub_id}), 500



@chefs.route('/chefs/<int:chef_id>/region', methods=['GET'])
def get_chefs_in_same_state(chef_id):
    current_app.logger.info(f'GET /chefs/{chef_id}/region route')

    try:
        cursor = db.get_db().cursor()

        # Step 1: Get the state of the current chef
        cursor.execute("SELECT StateName FROM Chef WHERE ChefID = %s", (chef_id,))
        result = cursor.fetchone()

        if not result or not result[0]:
            return jsonify({"error": "Chef not found or state information missing"}), 404

        state = result[0]

        # Step 2: Find other chefs in the same state (excluding the current chef)
        query = """
            SELECT ChefID, FirstName, LastName, CuisineSpecialty, YearsExp, City, StateName, Country
            FROM Chef
            WHERE StateName = %s AND ChefID != %s;
        """
        cursor.execute(query, (state, chef_id))
        chefs = cursor.fetchall()

        # Step 3: Format the result as JSON
        columns = [desc[0] for desc in cursor.description]
        chef_list = [dict(zip(columns, row)) for row in chefs]

        return jsonify(chef_list), 200

    except Exception as e:
        db.get_db().rollback()
        return jsonify({"error": str(e)}), 500


@recipes.route('/chefs/<int:chef_id>/recipes', methods=['GET'])
def get_chef_recipes(chef_id):
    try:
        # Connect and create a cursor
        conn = db.get_db()
        cursor = conn.cursor()

        # Safe, simple query
        cursor.execute("""
            SELECT 
                RecipeID, RecipeName, NumShares, NumViews, NumReviews, 
                IsFeatured, PublishDate
            FROM Recipe
            WHERE ChefID = %s
        """, (chef_id,))

        # Fetch rows
        rows = cursor.fetchall()

        # Create proper JSON response
        response = make_response(jsonify(rows))
        response.mimetype = 'application/json'
        response.status_code = 200
        return response

    except Exception as e:
        # Fail safe
        print("Error:", str(e))
        return jsonify({"error": "Something went wrong."}), 500

@recipes.route('/recipes/<int:recipe_id>/del', methods=['DELETE'])
def delete_recipe(recipe_id):
    current_app.logger.info(f'DELETE /recipes/{recipe_id} route')

    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Then delete the recipe itself
        cursor.execute("DELETE FROM Recipe WHERE RecipeID = %s;", (recipe_id,))

        # First delete related entries in Newsletter
        cursor.execute("DELETE FROM Newsletter WHERE RecipeID = %s;", (recipe_id,))

        conn.commit()

        return jsonify({"message": f"Recipe with ID {recipe_id} successfully deleted."}), 200

    except Exception as e:
        db.get_db().rollback()
        current_app.logger.error(f"Error deleting recipe: {e}")
        return jsonify({"error": str(e)}), 500


        