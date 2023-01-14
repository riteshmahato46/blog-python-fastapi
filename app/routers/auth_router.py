from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models import auth_models
from ..authentication import oauth2
from ..authentication import auth_utils
from ..persistence import database, db_models

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=auth_models.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    '''
    Summary:
    Login a user into the system.

    Parameters[Form]:
    username, password

    Returns:
    The 'access token' and 'type' for a successful login and 403 Error for invalid credentials
    '''
    #Get the user from the database
    user = db.query(db_models.User).filter(db_models.User.email == user_credentials.username).first()
   
   # If user does not exist in database, throw 403 Exception
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials for user {user_credentials.email}")

    # If the password is incorrect, throw 403 Exception
    if not auth_utils.verify_password(user_credentials.password, user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials for user {user_credentials.email}")

    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}