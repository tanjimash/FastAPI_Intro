from passlib.context import CryptContext


# Func instance for hashing the password, displayed in the response-body
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt_hash( password:str ):
        # hash the password
        return pwd_ctx.hash( password )
    

    def verify( plain_pass, hashed_pass ):
        return pwd_ctx.verify( plain_pass, hashed_pass )