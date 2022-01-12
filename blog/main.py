from fastapi import FastAPI
from starlette import responses
from starlette.responses import Response
import schemas, models
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from hash import Hash
from routers import blog, user, authentication
# from routers import router




# the methods used for interacting with the database are required to use the "db" param to fetch the DB-instance.


# create the fastapi object
app = FastAPI()


# Define the route explicitly, so that it can get the token to be beared using the "OAuth2PasswordBearer" method.
# oauth2_scheme = OAuth2PasswordBearer( tokenUrl='token' )


# Include all the route files from the "routers" directory.
# app.include_router( router.blog )
# attach "router" along with the route-file names
app.include_router( authentication.router )
app.include_router( blog.router )
app.include_router( user.router )



# migration command for the database
# [ RESPONSIBLE ]: for creating/ updating db-table
models.Base.metadata.create_all( engine )   # db will be created in the current directory "/blog/"


# The func for getting the db-session is moved to the "database.py" file.


# All the path-operation APIs are moved to the "route" files in the "routers" directory.

# The api-routes are divided into two route-files.
#   "blogs.py"
#   "user.py"






