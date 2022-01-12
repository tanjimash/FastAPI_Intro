from fastapi import APIRouter, Depends, status, HTTPException
import schemas, models
from database import get_db
from sqlalchemy.orm import Session
from hash import Hash
from datetime import datetime, timedelta
from jwt_token import create_access_token
from fastapi.security import  OAuth2PasswordRequestForm
from oauth2 import get_current_user as gcu




router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

# ######################################
# Generate JWT token whenever the login is successful.
# ######################################


@router.post( '/loginAPI' )
# def login( request: schemas.Login, db: Session = Depends( get_db ) ):
def login( request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends( get_db ) ):
    # print( request )

    # fetch & filter the user email from teh db-model user, the email will the known as "username" in the pydantic model-class ("Login")
    # Pass the email of a user inside the "username" of the "request-body" in the browser.
    user = db.query( models.User ).filter( models.User.email == request.username ).first()

    # print( user.id )
    # print( user.name )
    # print( user.email )
    # print( user.password )


    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Invalid Credentials!'
        )

    # print( 'Plain pass: ', request.password )
    # print( 'Hashed pass: ', user.password )

    # check if the hashed_pass & the plain_pass gets verified.
    if not Hash.verify( request.password, user.password ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Invalid Password!'
        )


    # #############################
    # generate JWT token & return
    # #############################
    # If the password is verified, then create the jwt access token.
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    access_token_expire = timedelta( minutes=ACCESS_TOKEN_EXPIRE_MINUTES )


    # call the "create_access_token()" method from the "jwt_token.py" file & assign that token inside a variable.
    # Syntax =>   create_access_token( data={ 'sub':username }, expire_delta=access_token_expires )
    access_token = create_access_token(
        data={ 'sub': user.email },
        expire_delta=access_token_expire
    )

    context = {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user,
    }

    return context
