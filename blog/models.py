from database import Base
from sqlalchemy import Column, Integer, String


# This class-models extends the class "Base" from the "database.py" file.

# Create the database-model
class Blog(Base):
    __tablename__ = 'blogs'     # table-name; which will be displayed in the Database

    id = Column( Integer, primary_key=True, index=True )
    title = Column( String )
    body = Column( String )



# from sqlalchemy.ext.declarative import declarative_base
# # Declare the mapping (db-table mapping)
# Base = declarative_base()
