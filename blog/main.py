from fastapi import FastAPI
from .schemas import *


# FastAPI Obj
app = FastAPI()


# [ IMPORATNT ]: Database Connection will be established after here. 
# Database connection will be built inside the "database.py" file.


# The blog-class-model is moved to the "schemas.py" file.








# Create a new blog, ( alter store that inside a database )
@app.post( '/subfolder/blog/' )
def create_blog( request:Blog ):
    context = {
        'msg': 'Create a new blog',
        'request': request,
    }
    return { 'data': context }

