# [ NOTE ]  The database connection will be established in this file.
#   Also the database-engine will be established.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base     # declare the mapping
from sqlalchemy.orm import sessionmaker     # create session


# ###############################
# [ NOTE ] Create the database-engine
#   Declare a mapping
# ###############################


# [ Syntax ]:  create_engine( 'database_path',  connect_args={ "check_same_thread":False } )

# Create the database inside the working-file-directory:  "database.db"

# Database_URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Create DB-engine
engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={ "check_same_thread":False } )


# Declare the mapping (db-table mapping)
Base = declarative_base()


# Create database session
SessionLocal = sessionmaker( bind=engine, autocommit=False, autoflush=False )

# Declare the mapping (db-table mapping)
Base = declarative_base()