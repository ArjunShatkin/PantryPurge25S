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
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
analysts = Blueprint('analysts', __name__)


#------------------------------------------------------------
# Get all customers from the system
@analysts.route('/recipes', methods=['GET'])
def get_recipes():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT I.IngredientName, Count(S.SearchID) as PastWeekSearches
FROM Ingredients I
NATURAL JOIN SearchIngredient SI
NATURAL JOIN Search S
WHERE S.SearchDate > NOW() - INTERVAL 7 DAY;
GROUP BY I.IngredientID
ORDER BY COUNT(S.SearchID) DESC

    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get list of most popular dietary restrictions by search
@analysts.route('/search/dietrestrict', methods=['GET'])
def get_searches():
    current_app.logger.info('GET /search/dietrestrict route')
    search_info = request.json
    days = search_info.get('days', 30)

    query = f'''SELECT D.RestName, Count(S.SearchID) as PastWeekSearches
FROM DietaryRestrictions D
NATURAL JOIN SearchDiet SI
NATURAL JOIN Search S
WHERE S.SearchDate > NOW() - INTERVAL {days} DAY
GROUP BY D.DietRestID
ORDER BY COUNT(S.SearchID) DESC
'''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get top searched ingredients in the past x days
@analysts.route('/search/ingredients', methods=['GET'])
def get_searches():
    current_app.logger.info('GET /search/ingredients route')
    search_info = request.json
    days = search_info.get('days', 30)

    query = f'''SELECT I.IngredientName, Count(S.SearchID) as PastWeekSearches
FROM Ingredients I
NATURAL JOIN SearchIngredient SI
NATURAL JOIN Search S
WHERE S.SearchDate > NOW() - INTERVAL {days} DAY;
GROUP BY I.IngredientID
ORDER BY COUNT(S.SearchID) DESC

'''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@analysts.route('/newsletter', methods=['GET'])
def get_searches():
    current_app.logger.info('GET /newsletter route')
    search_info = request.json
    days = search_info.get('days', 30)

    query = f'''SELECT Rec.Name, AVG(Rev.Rating) as AvgRating
FROM Recipe Rec
	NATURAL JOIN Review Rev
	JOIN Newsletter N ON Rec.RecipeID = N.RecipeID
WHERE N.SubDate > NOW() - INTERVAL {days} DAY
ORDER BY AvgRating DESC
'''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@analysts.route('/reviews', methods=['GET'])
def get_searches():
    current_app.logger.info('GET /reviews route')
    search_info = request.json
    maxrating = search_info.get('max_rating', 5)

    query = f'''SELECT Rev.ReviewText, Rev.Rating, Rec.Name
FROM Review Rev
	NATURAL JOIN Recipe Rec
WHERE Rev.Rating <= {maxrating}
'''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@analysts.route('/recipes/analytics', methods=['GET'])
def get_searches():
    current_app.logger.info('GET /recipes/analytics route')
    search_info = request.json
    days = search_info.get('days', 30)

    query = f'''SELECT Rec.Name, AVG(Rev.Rating) as AvgRating, COUNT(S.CookID) as Shares,
COUNT(OT.TrafficID) as OffsiteClicks
FROM Recipes Rec
	NATURAL JOIN Review Rev
	NATURAL JOIN Shares S
	NATURAL JOIN OffsiteTraffic OT
GROUP BY Rec.RecipeID
ORDER BY AvgRating DESC
'''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response