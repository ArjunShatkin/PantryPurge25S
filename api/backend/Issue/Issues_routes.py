from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
issues = Blueprint('issues', __name__)


# Get all the products from the database, package them up,
# and return them to the client
@issues.route('/issues', methods=['GET'])
def get_all_issues():

    cursor = db.get_db().cursor()
    
    query = '''
        SELECT  
         IssueID, UserID, EnteredTime, Priority,
         Status, Title, Description,
         ResolvedDate
        FROM Issue
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response


    

