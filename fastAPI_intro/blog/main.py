from fastapi import FastAPI
from .schemas import *
from . import models
# from database import engine

# FastAPI object
app = FastAPI()


# [ NOTE ]: The class-model "Blog" is moved to the file "schemas.py" file.



# [ IMPORTANT ]:  Create the DB connection using SQLAlchemy (SQL Toolkit & ORM).
#       use to create database-table using following code-line.
# models.Base.metadata.create_all(engine)   # define the DB-engine




@app.post( '/subfolder/blog/' )
# provide params using the pydnatic models, thus we can use this API to get 
# request-body from the user/ client.
# Now instead of getting simple-input-fields, we'll get "request-body" in the browser's swagger-UI.
def create_blog(request:Blog):
    context = {
        'msg': 'Creating a new blog',
        'request-body': request,
        # 'title': request.title,
        # 'body': request.body,
    }
    return { 'data': context }

