from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.authentication import oauth2
from app.persistence import database, db_models
from app.models import post_models

router = APIRouter(
    prefix="/like",
    tags=['Likes']
)

LIKE = 1
UNLIKE = 0

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: post_models.Like, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    '''
    Adds or removes a 'like' from a post.

        Parameters:
            like (Like): The like object containing post_id and direction (like = 1, unlike = 0)

        Returns:
            Success/Failure of the action
    '''
    # check whether the post exists
    post = db.query(db_models.Post).filter(db_models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {like.post_id} does not exist")
    
    # find out if the post is already liked by user
    already_liked_query = db.query(db_models.Like).filter(db_models.Like.post_id == like.post_id, 
                                     db_models.Like.user_id == current_user.id)
    already_liked_post = already_liked_query.first()
    
    if (like.direction == LIKE):
        # If the post is already liked by this user, we can't like again, throw 409 Conflict
        if already_liked_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"Post with id {like.post_id} already liked by user {current_user.id}")
        
        # Add like to the post in the databse
        new_like = db_models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": f"Successfully liked post {like.post_id}"}
   
    else: # User wants to unlike a post
        # If the post is not already liked by user, it can't be unliked
        if not already_liked_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post {like.post_id} is not liked by user {current_user.id}. Cannot unlike")
        
        # Remove the like from the post for this user
        already_liked_query.delete(synchronize_session=False)
        db.commit()
        return {"message": f"Successfully deleted like for post {like.post_id}"}