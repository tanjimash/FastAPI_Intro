from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker



# #######################
# Database Connection using SQLAlchemy
# #######################


# Database URL Constant
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# DB Engine
engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={ "check_same_thread":False } )


Base = declarative_base()


Session_local = sessionmaker( bind=engine, autocommit=False, autoflush=False )