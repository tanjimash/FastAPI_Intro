from pydantic import BaseModel



# #########################
#  This file is responsible for creating the frame to recieve the request body from the client.
# #########################


# Blog model Frame ( Pydantic model )
# Responsible for receiving the request-body from the client/ user/ browser.
# [ NOTE ]: It will help to get the request-body from the client/ user while the corresponding API.
class Blog(BaseModel):
    title: str
    body: str


