from pydantic import BaseModel


# #########################
#  This file is responsible for creating the frame to recieve the request body from the client.
# #########################


# Blog model Frame ( Pydantic model )
# In FastAPI, the pydantic models are called as "Schemas"
# Responsible for receiving the request-body from the client/ user/ browser.
# [ NOTE ]: It will help to get the request-body from the client/ user while the corresponding API.
class Blog(BaseModel):
    title: str
    body: str




# response-model class (used for "show specific blog detail" API)
# We can inherit/ extend the base-model for "Blog"
class blog_rModel(Blog):
    title: str
    body: str

    # [ NOTE ]: Since this class is interacting with the DB through SQLAlchemy ORM, 
    # so we need to explicitly define the orm_mode to True.
    class Config():
        orm_mode = True



