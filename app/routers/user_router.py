from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.models import user_models
from app.authentication import auth_utils
from app.persistence import db_models
from app.persistence.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=user_models.UserResponse)
def create_user(user:user_models.UserCreate, db: Session = Depends(get_db)):
    '''
    Creates a new user in the database.

        Parameters:
            user (UserCreate): the username and password

        Returns:
            A success or failure status
    '''
    # hash the password
    hashed_password = auth_utils.hash(user.password)
    user.password = hashed_password
    
    new_user = db_models.User(**user.dict())
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}", response_model=user_models.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    '''
    Fetches a user from the database.

        Parameters:
            id (int): The user id.

        Returns:
            UserResponse: The username and id.
    '''
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {id} not found")      
    return user