from pydantic import BaseModel


# #########################
#  This file is responsible for creating the frame to recieve the request body from the client.
# [ good practise ]:  use the "in" & "out" as suffix while creating the class-schemas.
#   for request-body class: use the "in" keyword as suffix.
#   for response-body (response-model) class: use the "out" keyword as suffix.
# #########################


# Blog model Frame ( Pydantic model )
# In FastAPI, the pydantic models are called as "Schemas"
# Responsible for receiving the request-body from the client/ user/ browser.
# [ NOTE ]: It will help to get the request-body from the client/ user while the corresponding API.
class Blog(BaseModel):
    title: str
    body: str



# "blog_rModel" is placed below the "User_rModel" to get the relation while defining the field "creator" in the "blog_rModel".


# Create a pydantic model called "User"
class User(BaseModel):
    name: str
    email: str
    password: str




class User_rModel(BaseModel):
    name:str
    email:str

    class Config():
        orm_mode = True





# response-model class (used for "show specific blog detail" API)
# We can inherit/ extend the base-model for "Blog"
class blog_rModel(BaseModel):
    title: str
    body: str
    creator_r: User_rModel

    # [ NOTE ]: Since this class is interacting with the DB through SQLAlchemy ORM, 
    # so we need to explicitly define the orm_mode to True.
    class Config():
        orm_mode = True
