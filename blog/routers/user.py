from fastapi import APIRouter, status, Depends, HTTPException
import schemas, models
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from starlette.responses import Response




# instantiate the router
router = APIRouter()





# Create new user
@router.post( 
    '/subfolder/user/', 
    status_code=status.HTTP_200_OK,
    tags=["Users"] )
def create_user( request:schemas.User, db: Session = Depends( get_db ) ):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt_hash( request.password ),
    )

    db.add( new_user )
    db.commit()
    db.refresh( new_user )  # refresh the "blog" table
    return new_user  # return the newly created blog from the db-table in the client-ui




# Get all the users
# If we want to apply the response model to where there are multiple queries provided as the response,
# then we are requried to qrap the response-model in a list.
@router.get(
    '/subfolder/user/', 
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.User_rModel], 
    tags=["Users"]
)
def user_list( db: Session = Depends( get_db ) ):
    user = db.query( models.User ).all()
    return user




# Fetch a psecific user information
@router.get( 
    '/subfolder/user/{id}', 
    status_code=status.HTTP_200_OK,
    response_model=schemas.User_rModel, 
    tags=["Users"] )
def get_individual_user_detail( id, response: Response, db: Session = Depends( get_db ) ):
    user = db.query( models.User ).filter( models.User.id == id ).first()
    
    # assigning appropriate status-code while handling error.
    # check if there is any such blog available
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { 'data': f'Blog with the {id} is not available!' }   # provide a response msg

        # Intead of using the aforementioned two things, use the HTTPException imported from the "fastapi"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Blog with the {id} is not available!'
        )
    return user




# Update a specific user
@router.put( 
    '/subfolder/user/{id}', 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Users"] )
# Make a request-body for the client (schemas) & fetch the db-session-model instance
def update_blog( id, request: schemas.User, db: Session = Depends( get_db ) ):
    user = db.query( models.User ).filter( models.User.id == id ).first()
    
    # Raise exception: if no such user is available with that ID.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No such user with id {id} is available!'
        )

    # Update the model-instance field using the client's request-body-field (schema - from the browser)
    user.name = request.name
    user.email = request.email
    user.password = request.password

    db.commit()
    # # after committed updation, refresh the db.
    db.refresh( user )
    # # provide the updated user object (fetched from the db again).

    return { 
        'msg': 'User detail is updated!',
        'User (Updated)': user,
    }





# Delete a specific user
# [ NOTE ]: when the status-code 204 is used, nothing will be returned as response
@router.delete( 
    '/subfolder/user/{id}', 
    status_code=status.HTTP_204_NO_CONTENT, 
    tags=["Users"] )
# @app.delete( '/subfolder/blog/{id}', status_code=204 )
# @app.delete( '/subfolder/blog/{id}' )
def delete_blog( id, db: Session=Depends( get_db ) ):
    # make a query from the "User" model & filter based on the "ID"
    # search for the user-obj from the db-model "User"
    user = db.query( models.User ).filter( models.User.id == id )
    
    # Raise exception: if no such blog is available with that ID.
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No such user with id {id} is available!'
        )
    
    user.delete( synchronize_session=False )
    db.commit()  

