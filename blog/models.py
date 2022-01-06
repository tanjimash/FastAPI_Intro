from sqlalchemy.sql.schema import ForeignKey
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship



# This class-models extends the class "Base" from the "database.py" file.

# Create the database-model
class Blog(Base):
    __tablename__ = 'blogs'     # table-name; which will be displayed in the Database

    id = Column( Integer, primary_key=True, index=True )
    title = Column( String )
    body = Column( String )
    user_id = Column( Integer, ForeignKey( "users.id" ) )  # [ NOTE ]:  use the "tableName.fieldName" while defining the foreignKey.

    # Syntax = ( modelName, back_populates="relationshipFieldName" )
    creator_r = relationship( "User", back_populates='blog_r' )   # define using the "users" tableName of the model "User".




class User(Base):
    __tablename__ = 'users'     # table-name; which will be displayed in the Database

    id = Column( Integer, primary_key=True, index=True )
    name = Column( String )
    email = Column( String )
    password = Column( String )

    # Syntax = ( modelName, back_populates="relationshipFieldName" )
    blog_r = relationship( "Blog", back_populates="creator_r" )
