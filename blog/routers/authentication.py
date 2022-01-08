from fastapi import APIRouter, Depends, status, HTTPException
import schemas, models
from database import get_db
from sqlalchemy.orm import Session



router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)



@router.post( '/' )
def login( request: schemas.Login, db: Session = Depends( get_db ) ):
    # print( request )


    # fetch & filter the user email from teh db-model user, the email will the known as "username" in the pydantic model-class ("Login")
    # Pass the email of a user inside the "username" of the "request-body" in the browser.
    user = db.query( models.User ).filter( models.User.email == request.username ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Invalid Credentials'
        )

    return user

