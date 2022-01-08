from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status




# get all blogs
def get_all_blog( db: Session ):
    # [ Query: get all rows ] make a query to get all the rows of blogs from the DB
    blogs = db.query( models.Blog ).all()
    return blogs





# get an individual blog
def get_blog_detail( id, db: Session ):
    blog = db.query( models.Blog ).filter( models.Blog.id == id ).first()
    
    # assigning appropriate status-code while handling error.
    # check if there is any such blog available
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { 'data': f'Blog with the {id} is not available!' }   # provide a response msg

        # Intead of using the aforementioned two things, use the HTTPException imported from the "fastapi"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Blog with the {id} is not available!'
        )
    return blog




# create a new blog
def create_b( request: schemas.Blog, db: Session ):
    # Create the frame ( Schema ) according to the model-field of the class "Blog".
    # create the instance of the request-data using inside the model-instance according to the models-fields.
    new_blog = models.Blog( title=request.title, body=request.body, user_id=1 )
    db.add( new_blog )  # add the new data-row
    db.commit()  # save/ commit the addition of the new data
    db.refresh( new_blog )  # refresh the "blog" table
    return new_blog  # return the newly created "blog" model from the db-table in the client-ui





# update a blog detail
def update_b( id, request: schemas.Blog, db: Session ):
    blog = db.query( models.Blog ).filter( models.Blog.id == id ).first()
    
    # Raise exception: if no such blog is available with that ID.
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No such blog with id {id} is available!'
        )

    # Update the model-instance field using the client's request-body-field (schema - from the browser)
    blog.title = request.title
    blog.body = request.body

    db.commit()
    # # after committed updation, refresh the db.
    db.refresh( blog )
    # # provide the updated blog object (fetched from the db again).

    return { 
        'msg': 'The blog is updated!',
        'Blog (Updated)': blog,
    }





# delete a blog
def del_blog( id, db ):
    # make a query from the "Blog" model & filter based on the "ID"
    # search for the blog-obj from the db-model "Blog"
    blog = db.query( models.Blog ).filter( models.Blog.id == id )
    
    # Raise exception: if no such blog is available with that ID.
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'No such blog with id {id} is available!'
        )
    
    blog.delete( synchronize_session=False )
    db.commit()     # after deleting a row, it's required to make commit


    # [ NOTE ] if the status-code 204 is used, nothing can be returned as response-body
    # return 'The blog is deleted!'
    # return { 'msg': f'The blog with the id {id} is deleted!' }

    # refer to the documentation of SQLAlchemy
    # Ref:  https://docs.sqlalchemy.org/en/14/orm/query.html?highlight=delete#sqlalchemy.orm.Query.delete
    #  Instead of fetching the first-data-row, will use the "delete()" operation.
