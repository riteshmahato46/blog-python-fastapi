from pydantic import BaseModel
from datetime import datetime
from .user_models import UserResponse

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
  
class PostResponse(Post):
    created: datetime
    id: str
    user_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True
   
class PostLikesResponse(BaseModel):
    Post: PostResponse
    likes: int
    
    class Config:
        orm_mode = True
    
class Like(BaseModel):
    post_id: int
    direction: int  # direction is 1 or 0 (like/unlike)