from fastapi import FastAPI
from pydantic import BaseModel

# FastAPI Obj
app = FastAPI()


# Blog model
# [ NOTE ]: It will help the get the request-body from the client/ user while the corresponding API.
class Blog(BaseModel):
    title: str
    body: str



# Create a new blog, ( alter store that inside a database )
@app.post( '/subfolder/blog/' )
def create_blog( request:Blog ):
    context = {
        'msg': 'Create a new blog',
        'request': request,
    }
    return { 'data': context }

