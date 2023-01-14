from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..persistence import database, models
from .. import schemas, oauth2

router = APIRouter(
    prefix="/like",
    tags=['Likes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    # check whether the post exists
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {like.post_id} does not exist")
    
    # find out if the post is already liked by user
    already_liked_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, 
                                     models.Like.user_id == current_user.id)
    already_liked_post = already_liked_query.first()
    
    if (like.direction == 1):
        if already_liked_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"Post with id {like.post_id} already liked by user {current_user.id}")
        
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": f"Successfully liked post {like.post_id}"}
   
    else:
        if not already_liked_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Like does not exist")
        
        already_liked_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"Successfully deleted like for post {like.post_id}"}