from fastapi import FastAPI
from typing import Optional


# object of FastAPI
app = FastAPI()


@app.get( '/' )
def index():
    context = {
        'title': 'Homepage API',
    }
    return { 'data': context }




@app.get( '/about/' )
def about():
    context = {
        'title': 'About Page API',
    }
    return { 'data': context }





# ---------------> Handling the Query-Parameter

# [ IMPORTANT ]:  FastAPI is smart enough to differentiate between the path-param & the query-param.



# [ NB ]:  fetchinh all the blogs from the DB is super inefficient,
#   so we can use "query-parameter" in the path-string.
#   not required to define the queries in the path-string here, 
#   but to accept in the func, we need to define them as params.
#   define default values for parameters of the func. 
#   [ IMPORTANT ]: If we can't set default value for a single parameter leaving all the others without a default value, thus all other params are also required to be set with default values.
#   [ NOTE ]: If we don't want to set a default value to a parameter, then we define that param with the "Optional" keyword & the data-type of that param. "Optional" class needs to be imported from the module "typing".
@app.get( '/blog/' )
def blogList(limit=10, published:bool=False, sort: Optional[str]=None):
    context = {
        'title': 'Blog List API',
    }
    if published:
        context['Blog List - Published'] = f'{limit} published blogs from the DB'
    else:
        context['Blog List - All'] = f'{limit} blogs from the DB'
    return { 'data': context }




@app.get( '/blog/unpublished' )
def blogUnpublished():
    context = {
        'title': 'Blog List API',
    }
    return { 'data': context }







# ------------------------------
# ALL THE DYNAMIC ROUTING SHOULD BE PLACED IN THE BOTTOM OF THE ORDERING, 
# OTHERWISE, THEY WILL MAKE CONFLICT WITH THE OTHER ROUTES.
# ------------------------------




# [NB]: for dynamic routing, use any routing-variable inside the second-bracket "{}"
#   To pass the routing0variable inside the function, use func-params.
#   Require to define the "id" as string in the method-parameter
@app.get( '/blog/{id}/' )
def blogDetail(id:int):
    context = {
        'title': 'Blog Detail API',
        'Blog ID': id,
    }
    return { 'data': context }




# blog-comments
@app.get( '/blog/{id}/comments/' )
def blogComments(id:int):
    comments = { '1','2', '3', '4', '5' }
    context = {
        'title': 'Blog Detail - Comments API',
        'Blog ID': id,
        'Blog Comments': comments,
    }
    return { 'data': context }




# --------------------> Request Body & Response Body
# [ IMPORTANT ]: When we send data from a client to our API, we send it as a "request body".
#   A "request body" is the data send from the client to our API.
#   A "response body" is the data send from our API to the client.

# [ IMPORTANT ]: To use a "request body", we need to use the "pydantic models".
#   Thus, we need to import the "BaseModel" from the "pydantic" model. Then generate a model class, 
#   which will be extended by the specific fuonction, which requires to use a request-body.

from pydantic import BaseModel


# "Blog" model, which will be used as a request-body inside the "create_blog" func.
# [ Note ]: models are similar to the db-tables
class Blog(BaseModel):
    title: str
    blog: str
    published: Optional[bool]   # not a required-field



# Create new blog
# The request-body needs to be defined inside the func-param, where we also have to define the model-class-name.
# Now we can get the data from the user/ client to our API.
@app.post( '/blog/' )
def create_blog(request:Blog):
    context = {
        'title': 'Craete new blog API',
        'message': 'A new blog is created!',
    }
    return { 
        'data': context,
        'request-body': request,
    }
