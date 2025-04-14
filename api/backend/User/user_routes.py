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
issues = Blueprint('issues', __name__)


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
    return 'user updated'


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


# Get all the products from the database, package them up,
# and return them to the client
@issues.route('/issues', methods=['GET'])
def get_all_issues():

    cursor = db.get_db().cursor()
    
    query = '''
        SELECT IssueID, UserID, EnteredTime, Priority, Status, Title, Description, ResolvedDate   
        FROM Issues
        
    '''
  
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response

# This is a POST route to add a new product.
# Remember, we are using POST routes to create new entries
# in the database. 
@issues.route('/product', methods=['POST'])
def add_new_issue():
    
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    issue_number = the_data['issueid']
    person = the_data['userid']
    description = the_data['description']
    title = the_data['Title']
    status = the_data['Status']
    priority = the_data ['Priority']
    
    query = f'''
        INSERT INTO products (issueid, userid,
                              description,
                              Title, Status, priority)
        VALUES ('{issue_number}','{person}', '{description}', '{title}', '{status}','{priority}')
    '''
 
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added issue")
    response.status_code = 200
    return response



@issues.route('/issues/<issueid>', methods=['Delete'])
def delete_issue():

    the_data = request.json
    current_app.logger.info(the_data)
    
    issue_number = the_data['issueid']
    
    query = '''
        Select *
        from Issue
        where issueid = {issue_number}
    '''
   
    # executing and committing the delete statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().delete()
    
    response = make_response("Successfully deleted issue")
    response.status_code = 200
    return response
    

    
    


    

