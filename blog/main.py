from fastapi import FastAPI, Depends, status, HTTPException
from starlette import responses
from starlette.responses import Response
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from hash import Hash


# the methods used for interacting with the database are required to use the "db" param to fetch the DB-instance.


# create the fastapi object
app = FastAPI()


# migration command for the database
# [ RESPONSIBLE ]: for creating/ updating db-table
models.Base.metadata.create_all( engine )   # db will be created in the current directory "/blog/"




# get the session of the DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






# Create a new blog, ( alter store that inside a database )
# after establishing the DB connection, provide the db as session in the next-param.
# Convert the session into the pydantic model.
# The "db" param will be of SQLAlchemy's "Session" object. And default value of the type-object will be fetched from the "get_db()" object.
# @app.post( '/subfolder/blog/', status_code=201 )
@app.post( 
    '/subfolder/blog/', 
    status_code=status.HTTP_201_CREATED, 
    tags=["Blogs"] )
# [ NOTE ]: 'Session' alone is not a pydantic thing. Thus, it'll depend on the "SessionLocal" obj from the "database.py" file.
# Ref ( Brief Explanation of 'db: Session' param ):  https://www.youtube.com/watch?v=7t2alSnE2-I
# Time-Frame:  1:38:00
def create_blog( request: schemas.Blog, db: Session = Depends( get_db ) ):
    # Create the frame ( Schema ) according to the model-field of the class "Blog".
    # create the instance of the request-data using inside the model-instance according to the models-fields.
    new_blog = models.Blog( title=request.title, body=request.body, user_id=1 )
    db.add( new_blog )  # add the new data-row
    db.commit()  # save/ commit the addition of the new data
    db.refresh( new_blog )  # refresh the "blog" table
    return new_blog  # return the newly created "blog" model from the db-table in the client-ui




# while applying a schema-model to the respone-body where multiple-records exist,
# then we need to wrap that response-model with List[]. 
# [ NOTE ]:  List[] will be imported from the "typing" module.

# get blogs from the DB
# Using the response-model to display the response in customised manner.
@app.get( '/subfolder/blog/', 
        status_code=status.HTTP_200_OK,
        response_model=List[schemas.blog_rModel], 
        tags=["Blogs"] )
def get_all_blogs( db: Session = Depends( get_db ) ):
    # [ Query: get all rows ] make a query to get all the rows of blogs from the DB
    blogs = db.query( models.Blog ).all()
    return blogs





# Fetch data of a specific blog
# This func will provide an input field for "id".
@app.get( 
    '/subfolder/blog/{id}', 
    status_code=status.HTTP_200_OK,
    response_model=schemas.blog_rModel, 
    tags=["Blogs"] )    # cannot use spacing inside the 2nd bracket in the path-url
def get_individual_blog_detail( id, response: Response, db: Session = Depends( get_db ) ):
    blog = db.query( models.Blog ).filter( models.Blog.id == id ).first()
    
    # assigning appropriate status-code while handling error.
    # check if there is any such blog available
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { 'data': f'Blog with the {id} is not available!' }   # provide a response msg

        # Intead of using the aforementioned two things, use the HTTPException imported from the "fastapi"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Blog with the {id} is not available!'
        )
    return blog





# Delete a specific blog
# [ NOTE ]: when the status-code 204 is used, nothing will be returned as response
@app.delete( 
    '/subfolder/blog/{id}', 
    status_code=status.HTTP_204_NO_CONTENT, 
    tags=["Blogs"] )
# @app.delete( '/subfolder/blog/{id}', status_code=204 )
# @app.delete( '/subfolder/blog/{id}' )
def delete_blog( id, db: Session=Depends( get_db ) ):
    # make a query from the "Blog" model & filter based on the "ID"
    # search for the blog-obj from the db-model "Blog"
    blog = db.query( models.Blog ).filter( models.Blog.id == id )
    
    # Raise exception: if no such blog is available with that ID.
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No such blog with id {id} is available!'
        )
    
    blog.delete( synchronize_session=False )
    db.commit()     # after deleting a row, it's required to make commit


    # [ NOTE ] if the status-code 204 is used, nothing can be returned as response-body
    # return 'The blog is deleted!'
    # return { 'msg': f'The blog with the id {id} is deleted!' }

    # refer to the documentation of SQLAlchemy
    # Ref:  https://docs.sqlalchemy.org/en/14/orm/query.html?highlight=delete#sqlalchemy.orm.Query.delete
    #  Instead of fetching the first-data-row, will use the "delete()" operation.





# Update a specific blog
@app.put( 
    '/subfolder/blog/{id}', 
    status_code=status.HTTP_202_ACCEPTED, 
    tags=["Blogs"] )
# Make a request-body for the client (schemas) & fetch the db-session-model instance
def update_blog( id, request: schemas.Blog, db: Session = Depends( get_db ) ):
    blog = db.query( models.Blog ).filter( models.Blog.id == id ).first()
    
    # Raise exception: if no such blog is available with that ID.
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No such blog with id {id} is available!'
        )

    # Update the model-instance field using the client's request-body-field (schema - from the browser)
    blog.title = request.title
    blog.body = request.body

    db.commit()
    # # after committed updation, refresh the db.
    db.refresh( blog )
    # # provide the updated blog object (fetched from the db again).

    return { 
        'msg': 'The blog is updated!',
        'Blog (Updated)': blog,
    }



# ########################################
# >>>>>>>>>>>>>>>> Users <<<<<<<<<<<<<<<<
# ########################################


# Create new user
@app.post( 
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
@app.get(
    '/subfolder/user/', 
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.User_rModel], 
    tags=["Users"]
)
def user_list( db: Session = Depends( get_db ) ):
    user = db.query( models.User ).all()
    return user




# Fetch a psecific user information
@app.get( 
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
@app.put( 
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
@app.delete( 
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