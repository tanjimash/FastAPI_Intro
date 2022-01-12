from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends
import jwt_token as jt
# from fastapi.security import OAuth2PasswordBearer


# Define the route explicitly, so that it can get the token to be beared using the "OAuth2PasswordBearer" method.
# [ NOTE ]:  basically we need to define the login-api-url as the "tokenURL", in my case.
# oauth2_scheme = OAuth2PasswordBearer( tokenUrl='/auth/loginAPI/' )    # defining the login-route
# [ Alternatively ]
oauth2_scheme = OAuth2PasswordBearer( tokenUrl='auth/loginAPI' )    # defining the login-route


# Validate the auth-token
# this method will receiev a token-param which will depend upon the "oauth2_scheme".
def get_current_user( token: str = Depends( oauth2_scheme ) ):
    # HTTPException variable template
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # the token-varification-code is placed inside the "" file, the required elements for the following code-block is already inside the "jwtToken.py" file.
    return jt.verify_token( token, credentials_exception )


