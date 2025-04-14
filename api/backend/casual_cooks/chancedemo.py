########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from datetime import datetime
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
casual_cooks = Blueprint('casual_cooks', __name__)


#------------------------------------------------------------
# User Story 4.1
@casual_cooks.route('/recipes/match', methods=['POST'])
def recipe_match():
    data = request.json
    ingredients = data.get('ingredients')
    placeholder = ','.join(['%s'] * len(ingredients))

    query = f"""
        SELECT DISTINCT r.RecipeID, r.RecipeName, r.Description
        FROM Recipe r
        JOIN RecipeIngredient ri ON r.RecipeID = ri.RecipeID
        JOIN Ingredient i ON ri.IngredientID = i.IngredientID
        WHERE i.IngredientName IN ({placeholder})
    """

    current_app.logger.info('POST /recipes/match route; %s', ingredients)
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(ingredients))
    theData = cursor.fetchall()
    recipes = [{"RecipeID": row[0],
                "RecipeName": row[1],
                "Description": row[2]}
                for row in theData]
    cursor.close()
    the_response = make_response(jsonify(recipes))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# User Story 4.2
@casual_cooks.route('/recipes/filter', methods=['GET'])
def filter_recipes():
    prep_time_max = request.args.get('prep_time_max', type=int)
    cuisine = request.args.get('cuisine')
    diet_rest = request.args.get('diet_rest')

    query = """
        SELECT r.RecipeID, r.RecipeName, r.Description, r.PrepTimeMins, r.CookTimeMins, r.Cuisine
        FROM Recipe r
        LEFT JOIN DietRecipe dr ON r.RecipeID = dr.RecipeID
        LEFT JOIN DietaryRestrictions d ON dr.DietRestID = d.DietRestID
    """

    filters = []
    parameters = []

    if prep_time_max is not None:
        filters.append("r.PrepTimeMins <= %s")
        parameters.append(prep_time_max)
    if cuisine is not None:
        filters.append("r.Cuisine = %s")
        parameters.append(cuisine.strip())
    if diet_rest is not None:
        filters.append("d.DietRestName = %s")
        parameters.append(diet_rest.strip())

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY r.PrepTimeMins ASC;"

    current_app.logger.info('GET /recipes/filter route; prep_time_max: %s, cuisine: %s, diet_rest: %s',
                            prep_time_max, cuisine, diet_rest)
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(parameters))
    theData = cursor.fetchall()
    recipes_list = [{"RecipeID": row[0],
                     "RecipeName": row[1],
                     "Description": row[2],
                     "PrepTimeMins": row[3],
                     "CookTimeMins": row[4],
                     "Cuisine": row[5]}
                     for row in theData]
    cursor.close()
    the_response = make_response(jsonify(recipes_list))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# User Story 4.3
@casual_cooks.route('/cooks/<int:cook_id>/reviews', methods=['GET'])
def review_history(cook_id):
    query = """
        SELECT r.RecipeID, r.RecipeName, r.Description, rv.Rating, rv.ReviewDate
        FROM Recipe r
        JOIN Review rv ON r.RecipeID = rv.RecipeID
        WHERE rv.CookID = %s
        ORDER BY rv.ReviewDate DESC;
    """

    current_app.logger.info('GET /cooks/<int:cook_id>/reviews route')
    cursor = db.get_db().cursor()
    cursor.execute(query, (cook_id,))
    theData = cursor.fetchall()
    review_list = [{"RecipeID": row[0],
                    "RecipeName": row[1],
                    "Description": row[2],
                    "Rating": row[3],
                    "ReviewDate": row[4]}
                    for row in theData]
    cursor.close()
    the_response = make_response(jsonify(review_list))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# User Story 4.4
@casual_cooks.route('/cooks/<int:cook_id>/recommendations', methods=['GET'])
def recipe_recommendations(cook_id):
    query = """
        SELECT DISTINCT r.RecipeID, r.RecipeName, r.Description
        FROM Recipe r
        JOIN RecipeIngredient ri ON r.RecipeID = ri.RecipeID
        WHERE r.Cuisine IN (
            SELECT r2.Cuisine
            FROM Recipe r2
            JOIN Review rv ON r2.RecipeID = rv.RecipeID
            WHERE rv.CookID = %s
            AND rv.Rating >= 4
        )
        AND r.RecipeID NOT IN (
            SELECT rv.RecipeID
            FROM Review rv
            WHERE rv.CookID = %s
        )
        LIMIT 5;
    """

    current_app.logger.info('GET /cooks/<int:cook_id>/recommendations route')
    cursor = db.get_db().cursor()
    cursor.execute(query, (cook_id, cook_id))
    theData = cursor.fetchall()
    recommendations = [{"RecipeID": row[0],
                        "RecipeName": row[1],
                        "Description": row[2]}
                        for row in theData]
    cursor.close()
    the_response = make_response(jsonify(recommendations))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
    
#------------------------------------------------------------
# User Story 4.5
@casual_cooks.route('/recipes/<int:recipe_id>', methods=['GET'])
def recipe_details(recipe_id):
    query = """
        SELECT r.RecipeID, r.RecipeName, r.Description
        FROM Recipe r
        WHERE r.RecipeID = %s;
    """

    current_app.logger.info('GET /recipes/<int:recipe_id> route')
    cursor = db.get_db().cursor()
    cursor.execute(query, (recipe_id,))
    theData = cursor.fetchall()
    recipe_info = [{"RecipeID": row[0],
                   "RecipeName": row[1],
                   "Description": row[2]}
                    for row in theData]
    cursor.close()
    the_response = make_response(jsonify(recipe_info))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# User Story 4.6
@casual_cooks.route('/recipes/<int:recipe_id>/calories', methods=['GET'])
def recipe_calories(recipe_id):
    query = """
        SELECT
            r.RecipeID,
            r.RecipeName,
            r.Servings,
            i.IngredientName,
            i.CalPerUnit,
            i.MeasureUnit,
            ri.Quantity,
            ROUND((i.CalPerUnit * ri.Quantity), 2) as TotalIngredientCalories,
            ROUND((i.CalPerUnit * ri.Quantity) / r.Servings, 2) as CaloriesPerServing
        FROM Recipe r
        JOIN RecipeIngredient ri ON r.RecipeID = ri.RecipeID
        JOIN Ingredient i ON ri.IngredientID = i.IngredientID
        WHERE r.RecipeID = %s
        ORDER BY TotalIngredientCalories DESC;
    """

    current_app.logger.info('GET /recipes/<int:recipe_id>/calories')
    cursor = db.get_db().cursor()
    cursor.execute(query, (recipe_id,))
    theData = cursor.fetchall()
    recipe_cals = [{"RecipeID": row[0],
                    "RecipeName": row[1],
                    "Servings": row[2],
                    "IngredientName": row[3],
                    "CalPerUnit": row[4],
                    "MeasureUnit": row[5],
                    "Quantity": row[6],
                    "TotalIngredientCalories": row[7],
                    "CaloriesPerServing": row[8]}
                    for row in theData]
    cursor.close()
    the_response = make_response(jsonify(recipe_cals))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#------------------------------------------------------------
# User Story 4.7
@casual_cooks.route('/recipes/<int:recipe_id>/adjust', methods=['GET'])
def adjust_recipe(recipe_id):
    new_servings = request.args.get('new_servings', type=float)
    query = """
        SELECT
            r.RecipeID,
            r.RecipeName,
            r.Servings AS OriginalServings,
            i.IngredientName,
            ri.Quantity AS OriginalQuantity,
            ROUND(ri.Quantity * %s / r.Servings, 2) AS AdjustedQuantity
        FROM Recipe r
        JOIN RecipeIngredient ri ON r.RecipeID = ri.RecipeID
        JOIN Ingredient i ON ri.IngredientID = i.IngredientID
        WHERE r.RecipeID = %s;

    """

    current_app.logger.info('GET /recipes/<int:recipe_id>/adjust route')
    cursor = db.get_db().cursor()
    cursor.execute(query, (new_servings, recipe_id))
    theData = cursor.fetchall()
    cursor.close()
    adjusted = [{"RecipeID": row[0],
                 "RecipeName": row[1],
                 "OriginalServings": row[2],
                 "IngredientName": row[3],
                 "OriginalQuantity": row[4],
                 "AdjustedQuantity": row[5]}
                    for row in theData]
    the_response = make_response(jsonify(adjusted))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response