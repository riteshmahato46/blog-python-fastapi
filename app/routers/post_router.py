from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.authentication import oauth2
from app.models import post_models
from app.persistence import db_models
from app.persistence.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[post_models.PostLikesResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    '''
    Gets all the posts from the database.

        Parameters:
            No user params

        Returns:
            List[PostResponse] : A list of PostResponse types
    '''
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # SELECT posts.*, COUNT(likes.post_id) FROM posts LEFT OUTER JOIN likes ON posts.id = likes.post_id GROUP BY likes.post_id
    # Where posts.title LIKE %search% LIMIT limit OFFSET skip
    results = db.query(db_models.Post, func.count(db_models.Like.post_id).label("likes"))\
                .join(db_models.Like, db_models.Like.post_id == db_models.Post.id, isouter=True)\
                .group_by(db_models.Post.id).filter(db_models.Post.title.contains(search))\
                .limit(limit).offset(skip).all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_models.PostResponse)
def create_posts(post:post_models.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Creates a new post and stores it in the database.

        Parameters:
            post (Post): The new post to be created.

        Returns:
            new_post (PostResponse) : The newly created post
    '''
    # Add the user id to the post and store it in the database
    new_post = db_models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", response_model=post_models.PostLikesResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Fetches a post by its 'id' from the database.

        Parameters:
            id (int): The id of the post to be fetched.

        Returns:
            post (PostResponse) : The fetched post from db.
    '''
    # SELECT posts.*, COUNT(likes.post_id) FROM posts LEFT OUTER JOIN likes ON posts.id = likes.post_id GROUP BY likes.post_id
    # WHERE posts.id == id
    post = db.query(db_models.Post, func.count(db_models.Like.post_id).label("likes"))\
             .join(db_models.Like, db_models.Like.post_id == db_models.Post.id, isouter=True)\
             .group_by(db_models.Post.id).filter(db_models.Post.id == id).first()

    # If no post exists by this Id, then it cannot be liked, throw 404 NOT FOUND
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    
    # If the post is not created by the current user, it cannot be retrieved by this user
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Deletes a post by its 'id' from the database.

        Parameters:
           id (int): The id of the post to be deleted.

       Returns:
            No Response. Status code 204
    '''
    # SELECT * FROM posts WHERE posts.id == id
    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    # Get the first entry, no need to scan the table once we found an entry as id is primary key
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    # If the post was not created by the current user, they cannot delete the post
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=post_models.PostResponse)
def update_post(id: int, post: post_models.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Updates a post by its 'id' from the database.

        Parameters:
            id (int): The id of the post to be updated.

       Returns:
            post (PostResponse) : The updated post.
    '''
    # SELECT * FROM posts WHERE posts.id == id
    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    # Get the first entry as there cannot be duplicate post id, so stop scanning table
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    # A user can only update their own post, throw exception if post was not created by this user
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    
    return post
