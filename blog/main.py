from fastapi import FastAPI
from .schemas import *
from . import models
from .database import engine



# FastAPI Obj
app = FastAPI()


# [ IMPORATNT ]: Database Connection will be established after here. 
# Database connection will be built inside the "database.py" file.


# The blog-class-model is moved to the "schemas.py" file.



# [ Database-Model ]:  Create the tables inside the database.
# Create the database models, also the database-engine
# [ NOTE ]: whenever the application-server gets started, it's making a migration in the db-table.
models.Base.metadata.create_all( engine )





# Create a new blog, ( alter store that inside a database )
@app.post( '/subfolder/blog/' )
def create_blog( request:Blog ):
    context = {
        'msg': 'Create a new blog',
        'request': request,
    }
    return { 'data': context }

