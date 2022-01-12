from fastapi import APIRouter, status, Depends, HTTPException
import schemas, models, oauth2
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from starlette.responses import Response
from repository.user import *




# instantiate the router
# [ NOTE ]:  Use the tags param here intead of useing in every api-path-param
router = APIRouter(
    prefix='/user',
    tags=["User"]
)




# ########################################
# >>>>>>>>>>>>>>>> User <<<<<<<<<<<<<<<<
# ########################################





# Create new user
@router.post( 
    '/', 
    status_code=status.HTTP_200_OK )
def create_user( request:schemas.User, db: Session = Depends( get_db ),
    current_user: schemas.User = Depends( oauth2.get_current_user ) ):
    # all the function (path-operations) are moved to the "repository\user.py" path.
    return create_u( request, db )
    



# Get all the users
# If we want to apply the response model to where there are multiple queries provided as the response,
# then we are requried to qrap the response-model in a list.
@router.get(
    '/', 
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.User_rModel], 
)
def user_list( db: Session = Depends( get_db ),
    current_user: schemas.User = Depends( oauth2.get_current_user ) ):
    return all_users( db )




# Fetch a psecific user information
@router.get( 
    '/{id}/', 
    status_code=status.HTTP_200_OK,
    response_model=schemas.User_rModel )
def get_individual_user_detail( id, response: Response, db: Session = Depends( get_db ),
    current_user: schemas.User = Depends( oauth2.get_current_user ) ):
    return user_detail( id, db )




# Update a specific user
@router.put( 
    '/{id}/', 
    status_code=status.HTTP_202_ACCEPTED )
# Make a request-body for the client (schemas) & fetch the db-session-model instance
def update_user( id, request: schemas.User, db: Session = Depends( get_db ),
    current_user: schemas.User = Depends( oauth2.get_current_user ) ):
    # all the function (path-operations) are moved to the "repository\user.py" path.
    return update_user_detail( id, request, db )





# Delete a specific user
# [ NOTE ]: when the status-code 204 is used, nothing will be returned as response
@router.delete( 
    '/{id}/', 
    status_code=status.HTTP_204_NO_CONTENT )
# @app.delete( '/subfolder/blog/{id}', status_code=204 )
# @app.delete( '/subfolder/blog/{id}' )
def delete_blog( id, db: Session=Depends( get_db ),
    current_user: schemas.User = Depends( oauth2.get_current_user ) ):
    return delete_b( id, db )  

