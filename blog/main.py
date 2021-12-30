from fastapi import FastAPI, Depends
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


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
@app.post( '/subfolder/blog/' )
# [ NOTE ]: 'Session' alone is not a pydantic thing. Thus, it'll depend on the "SessionLocal" obj from the "database.py" file.
# Ref ( Brief Explanation of 'db: Session' param ):  https://www.youtube.com/watch?v=7t2alSnE2-I
# Time-Frame:  1:38:00
def create_blog( request: schemas.Blog, db: Session = Depends( get_db ) ):
    # Create the frame ( Schema ) according to the model-field of the class "Blog".
    # create the instance of the request-data according to the models-fields
    new_blog = models.Blog( title=request.title, body=request.body )
    db.add( new_blog )  # add the new data-row
    db.commit()  # save/ commit the addition of the new data
    db.refresh( new_blog )  # refresh the "blog" table
    return new_blog  # return the newly created blog from the db-table in the client-ui






# get blogs from the DB
@app.get( '/subfolder/blog/' )
def get_all_blogs( db: Session = Depends( get_db ) ):
    # [ Query: get all rows ] make a query to get all the rows of blogs from the DB
    blogs = db.query( models.Blog ).all()
    return blogs






@app.get( '/subfolder/blog/{id}' )    # cannot use spacing inside the 2nd bracket in the path-url
def get_individual_blog_detail( id, db: Session = Depends( get_db ) ):
    blog = db.query( models.Blog ).filter( models.Blog.id == id ).first()

    return blog
    return { 'msg': 'Fetch specific blog data' }
