from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt



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

    return jwt_token

