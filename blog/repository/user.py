from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from hash import Hash





# create new user
def create_u( request: schemas.Blog, db: Session ):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt_hash( request.password ),
    )

    db.add( new_user )
    db.commit()
    db.refresh( new_user )  # refresh the "blog" table
    return new_user  # return the newly created blog from the db-table in the client-ui





# get all the users
def all_users( db: Session ):
    user = db.query( models.User ).all()
    return user




# get a specific user detail
def user_detail( id, db: Session ):
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




# update a user detail
def update_user_detail( id, request: schemas.User, db: Session ):
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
    user.password = Hash.bcrypt_hash( request.password )  # hash the requested password

    db.commit()
    # # after committed updation, refresh the db.
    db.refresh( user )
    # # provide the updated user object (fetched from the db again).

    return { 
        'msg': 'User detail is updated!',
        'User (Updated)': user,
    }





# delete a user
def delete_b( id, db: Session ):
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
