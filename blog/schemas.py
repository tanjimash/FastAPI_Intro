from pydantic import BaseModel



# Blog model
# [ NOTE ]: It will help the get the request-body from the client/ user while the corresponding API.
class Blog(BaseModel):
    title: str
    body: str


