from pydantic import BaseModel


# pydantic model; thus require to extend the "BaseModel" from the "pydantic" module
class Blog(BaseModel):
    title:str
    body:str
