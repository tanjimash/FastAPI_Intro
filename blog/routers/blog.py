from fastapi import APIRouter, status, Depends, HTTPException
import schemas, models
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from starlette.responses import Response
from repository.blog import *



# instantiate the router
# [ NOTE ]:  Use the tags param here intead of useing in every api-path-param
router = APIRouter(
    prefix='/blog',
    tags=["Blog"] 
)





# ########################################
# >>>>>>>>>>>>>>>> Blog <<<<<<<<<<<<<<<<
# ########################################




# while applying a schema-model to the respone-body where multiple-records exist,
# then we need to wrap that response-model with List[]. 
# [ NOTE ]:  List[] will be imported from the "typing" module.

# get blogs from the DB
# Using the response-model to display the response in customised manner.
@router.get( 
    '/', 
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.blog_rModel] )
def get_all_blogs( db: Session = Depends( get_db ) ):
    # all the function (path-operations) are moved to the "repository\blog.py" path.
    return get_all_blog( db )





# Create a new blog, ( alter store that inside a database )
# after establishing the DB connection, provide the db as session in the next-param.
# Convert the session into the pydantic model.
# The "db" param will be of SQLAlchemy's "Session" object. And default value of the type-object will be fetched from the "get_db()" object.
# @app.post( '/subfolder/blog/', status_code=201 )
@router.post( 
    '/', 
    status_code=status.HTTP_201_CREATED )
# [ NOTE ]: 'Session' alone is not a pydantic thing. Thus, it'll depend on the "SessionLocal" obj from the "database.py" file.
# Ref ( Brief Explanation of 'db: Session' param ):  https://www.youtube.com/watch?v=7t2alSnE2-I
# Time-Frame:  1:38:00
def create_blog( request: schemas.Blog, db: Session = Depends( get_db ) ):
    # all the function (path-operations) are moved to the "repository\blog.py" path.
    # [ NOTE ]:  try to define the repo-funcs names distinctive.
    return create_b( request, db )
    








# Fetch data of a specific blog
# This func will provide an input field for "id".
@router.get( 
    '/{id}/', 
    status_code=status.HTTP_200_OK,
    response_model=schemas.blog_rModel )    # cannot use spacing inside the 2nd bracket in the path-url
def get_individual_blog_detail( id, response: Response, db: Session = Depends( get_db ) ):
    # all the function (path-operations) are moved to the "repository\blog.py" path.
    return get_blog_detail( id, db )
    









# Delete a specific blog
# [ NOTE ]: when the status-code 204 is used, nothing will be returned as response
@router.delete( 
    '/{id}/', 
    status_code=status.HTTP_204_NO_CONTENT )
# @app.delete( '/subfolder/blog/{id}', status_code=204 )
# @app.delete( '/subfolder/blog/{id}' )
def delete_blog( id, db: Session=Depends( get_db ) ):
    # all the function (path-operations) are moved to the "repository\blog.py" path.
    return del_blog( id, db )






# Update a specific blog
@router.put( 
    '/{id}/', 
    status_code=status.HTTP_202_ACCEPTED )
# Make a request-body for the client (schemas) & fetch the db-session-model instance
def update_blog( id, request: schemas.Blog, db: Session = Depends( get_db ) ):
    return update_b( id, request, db )


