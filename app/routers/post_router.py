from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import oauth2, schemas
from ..persistence import models
from ..persistence.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Summary:
    Gets all the posts from the database.

    Parameters:
    No user params

    Returns:
    List[PostResponse] : A list of PostResponse types
    '''

    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Summary:
    Creates a new post and stores it in the database.

    Parameters:
    post [schemas.Post]: The new post to be created.

    Returns:
    PostResponse : The newly created post
    '''

    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Summary:
    Fetches a post by its 'id' from the database.

    Parameters:
    id (int): The id of the post to be fetched.

    Returns:
    PostResponse : The fetched post from db.
    '''
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
        
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Summary:
    Deletes a post by its 'id' from the database.

    Parameters:
    id (int): The id of the post to be deleted.

    Returns:
    No Response. Status code 204
    '''
 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    Summary:
    Updates a post by its 'id' from the database.

    Parameters:
    id (int): The id of the post to be updated.

    Returns:
    PostResponse : The updated post.
    '''
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
