from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)


# Get all the products from the database, package them up,
# and return them to the client
@users.route('/users', methods=['GET'])
def get_all_users():

    cursor = db.get_db().cursor()
    
    query = '''
        SELECT  userid, 
                username, 
                datecreated, 
                UserStatus  
        FROM User
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response

@users.route('/users', methods=['PUT'])
def update_user():
    current_app.logger.info('PUT /users route')
    user_info = request.json
    user_id = user_info['UserId']
    user_name = user_info['Username']
    created = user_info['datecreated']
    status = user_info['UserStatus']

    query = 'UPDATE users SET user_name = %s,  status = %s where id = %s'
    data = (user_name, status, user_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'user updated!'

@users.route('/users/<datecreated>', methods=['GET'])
def creation_date_count():

    cursor = db.get_db().cursor()
    
    query = '''
        Select month(datecreated) as month, Count(*)
        from User
        group by month(DateCreated)
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response
    

