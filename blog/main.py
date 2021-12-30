from fastapi import FastAPI, Depends
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session





# create the fastapi object
app = FastAPI()


# migration command for the database
# [ RESPONSIBLE ]: for creating/ updating db-table
models.Base.metadata.create_all( engine )   # db will be created in the current directory "/blog/"




# get the session of the DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






# Create a new blog, ( alter store that inside a database )
# after establishing the DB connection, provide the db as session in the next-param.
# Convert the session into the pydantic model.
@app.post( '/subfolder/blog/' )
# [ NOTE ]: 'Session' alone is not a pydantic thing. Thus, it'll depend on the "SessionLocal" obj from the "database.py" file
def create_blog( request: schemas.Blog, db: Session = Depends( get_db ) ):
    # Create the frame ( Schema ) according to the model-field of the class "Blog".
    # create the instance of the request-data according to the models-fields
    new_blog = models.Blog( title=request.title, body=request.body )
    db.add( new_blog )  # add the new data-row
    db.commit()  # save/ commit the addition of the new data
    db.refresh( new_blog )  # refresh the "blog" table
    return new_blog  # return the newly created blog from the db-table in the client-ui
