from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.configuration.config import settings
from app.persistence import database, db_models
from app.models import auth_models

# To get a hex 32 string for this run: `openssl rand -hex 32`
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    '''
    Creates a new access token.

        Parameters:
            data: contains the user_id for which the access token is to be generated

        Returns:
            encoded_jwt (JWT): The jwt access token
    '''
    to_encode = data.copy()
    
    # make sure it's datetime.utcnow(). if it's just now(), it will error in unit test
    expiry_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry_time})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    '''
    Verifies if an access token is valid.

        Parameters:
            token (str): The token to be verified.
            credentials_exception (HTTPException): The exception to be thrown in case of invalid token

        Returns:
            token_data (TokenData): The data encoded in the token (user_id)
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = auth_models.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    '''
    Fetches the current logged in user after validating the JWT token.

        Parameters:
            token (str): The token to be verified.
    
        Returns:
            user (User): The user object from the database
    '''
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    # SELECT * FROM users WHERE users.id == token.id
    user = db.query(db_models.User).filter(db_models.User.id == token.id).first()
    
    return user