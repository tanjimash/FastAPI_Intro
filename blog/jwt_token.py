from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import schemas


# # [ Important Elements ]: to encode the JWT Access Token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30   # this expiry is created inside the "authentication.py" file.




# # jwt-token creation method
def create_access_token( data: dict, expire_delta: Optional[ timedelta ]=None ):
    # make a copy of the dictionary data (typically consist of user-email).
    to_encode = data.copy()

    # check if the expiry-time is provided, make sure to get the expiry-time is converted into "timedelta" format.
    if expire_delta:
        #  assign the expiry time with the current time
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta( minutes=15 )

    # then update ( add new key-value pair ) the data-dict with the token-expiration ( formatted with the 'timedelta' func )
    to_encode.update( { 'exp': expire } )

    # the jwt.encode func consist of three things: a dict, the secret_key & the algorithm.
    # the dict should be consist of two key-value pair:  username, expiration-time
    jwt_token = jwt.encode( to_encode, SECRET_KEY, ALGORITHM )

    print( 'Generated Token: ', to_encode )

    return jwt_token







# verify the token, is called from the "oauth2.py" file's method called "get_current_user()".
# "token" is passed from where it's called, means inside the "get_current_user()" method.
# The param called "credentials_exception" is created inside the "get_current_user()" method.
def verify_token( token: str, credentials_exception ):
    # try to decode the jwt-token
    try:
        # the "token" is passed from the "get_current_user()" method ( from the 'blog\oauth2.py' file ) where this "verify_token()" method is called.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print( 'Decoded Token (Payload): ', payload )

        # if the token is decoded, then get the decoded key-value pair using the key called "sub"
        # the "sub" key is fetched, because the token is generated using the user-email is constructed using the key called "sub".
        email: str = payload.get("sub")
        # print( 'Email:', email )

        # if there is no value inside the variable "email", then raise exception
        if email is None:
            raise credentials_exception
        
        # [ IMPORATNT OBJECTIVE ]: extract the user-email fom the decoded-token & then pass that to the schema-model "TokenData".
        # it's a schema, which is created earlier inside the "schemas.py" file.
        token_data = schemas.TokenData(email=email)

        # return token_data
    except JWTError:
        raise credentials_exception
