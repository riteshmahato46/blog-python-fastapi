
from pydantic import BaseModel,EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostResponse(BaseModel):
    title: str
    content: str
    published: bool = True
    
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    
    class Config:
        orm_mode = True