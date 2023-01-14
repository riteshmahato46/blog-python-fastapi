from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created: datetime
    
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
   