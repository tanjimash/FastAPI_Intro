# FastAPI Intro

"""
[ Notes ]
# FastAPI reads the file line-by-line. So there might rise issues with the routing, i.e. the blog-detail api is expecting an integer as ID after the keyword "blog".
    So to have other APIs regarding the keyword "blog", then we should use the the other keywords before the keyword "blog"
"""


from fastapi import FastAPI
from typing import Optional     # used for passing optional paramters in the path-operation-functions (methods)
# from pydantic import 
from pydantic import BaseModel




# isntance of "FastAPI", used for decorating the methods.
app = FastAPI()


# This method will handle the Path using FastAPI using a decorator

# The default path of a url is a slash ("/").
# homepage-api
# Decorator Syntax:  path_operation_decorator.operation( 'path' )
@app.get( '/' )
# It's called the path-operation-function
def index():
    # return "Hellow!"
    
    # since, we widely accept JSON for the APIs.
    context = {
        'name': 'Homepage',
    }
    return { 'data': context }  # passing dict, like a JSON 




# about-api
@app.get( '/about/' )
def about():
    context = {
        'title': 'About Page',
    }
    return { 'data': context }




# Blog List API
# [ NB ]:  to get all the blogs from the DB, is not efficient. 
# Thus we can pass the query limit, as well as other params.
# [ Query-paramter is required to use while hitting this API ] -- Queries: ("limit", "published")
# All the parameters are required to satisfy in the routing-url while trying to hit for the specific API.
# Require to define using the type-castinf inside the parameters of the method. i.e. Need to specify the "published" parameter as boolean, we need to define that using the colon & keyword "bool"
# Pass an OPTIONAL PARAMETER called "sort"
@app.get( '/blog/' )
def blogList(limit=10, published: bool = False, sort: Optional[str] = None):
    context = {
        'title': 'Blog Page',
        # 'blogList': f'{limit} Blogs from the DB',
    }
    # if "True/ False" is passed in the query param
    if published:
        context['blogList'] = f'{limit} published blogs from the DB'
    else:
        context['blogList'] = f'{limit} blogs from the DB'
        
    return { 'data': context }




# Blog Detail API
@app.get( '/blog/{id}/' )  # dynamically pass the id in the API-routing
# then the id need to be passed inside the func thorugh a param ("id")
# define/ convert the id as integer in the method's parameter.
def blogDetail(id: int):
    # fetch blog using the id which is set inside the path.   [ id = id ]
    context = {
        'title': 'Blog Page',
        'blog_id': id,
    }
    return { 'data': context }




# Unpublished Blog List API
@app.get( '/unpublished/blog/' )
def unpublishedBlogList():
    context = {
        'title': 'Unpublished Blog Page',
    }
    return { 'data': context }
"""
[ NB ]: if anther string is addded after the keyword "/blog/" then it'll throw an error, 
    cause the previous api is leading to an integer as ID.
"""





"""
pydantic models provide us with the models similar to ORM. BUt to use "pydantic models" we've to extend 
our method with the "BaseModel" provided by the "pydantic" module itself.
"""


# pydantic model
# This model will be used inside the parameter of "createBlog" function.
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[ bool ]




# Blog Create API
# [ NB ]:  When we want to send data from a client (i.e. browser) to our API, then we send it using a 'request-body'.
#       A request-body is the data to send to the client from the API & vice versa.
# [ IMPORTANT ] To declare a 'request-body', we use "pydantic" models.
# Require to pass the pydantic model className ("Blog") in the function in order to use the request-body sent from the clienr.
# We need to define the "request" keyword as well inside the parameter.
@app.post( '/blog/' )
def createBlog( request: Blog ):
    context = {
        'title': 'A new blog is created',
    }
    return request
    return { 'data': context }



