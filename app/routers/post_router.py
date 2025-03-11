from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..entities.post_entity import Post
from ..entities.user_entity import User
from ..entities.vote_entity import Vote
from ..schemas.post_schema import (CreatePostRequestDto, PostDto,
                                   PostDtoWithVotes)
from ..schemas.token_schema import TokenData
from ..schemas.user_schema import UserDto
from ..utils.jwt import get_current_token_payload, get_current_user
from ..utils.utils import only_owner_action

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostDto)
def create_post(post: CreatePostRequestDto, db:Session = Depends(get_db), token_data: TokenData = Depends(get_current_token_payload)):
    # with psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
    #     with conn.cursor(row_factory = dict_row) as cursor:
    #         cursor.execute(
    #             """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #             (postDict['title'], postDict['content'], postDict['published']))
    #         new_post = cursor.fetchone()
    new_post = Post(user_id=token_data.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("", response_model=List[PostDtoWithVotes])
def get_all_posts(db:Session = Depends(get_db), token_data: TokenData = Depends(get_current_token_payload), limit: int = 10, skip: int = 0, search: Optional[str] = ''):  
    # with psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
    #     with conn.cursor(row_factory = dict_row) as cursor:
    #         cursor.execute("""SELECT * FROM posts""")
    #         posts = cursor.fetchall()
    query = db.query(Post, func.count(Vote.post_id).label("votes")).outerjoin(Vote, Vote.post_id == Post.id).group_by(Post.id).order_by("votes").filter(Post.title.ilike(f"%{search.strip()}%")).limit(limit).offset(skip)
    posts = query.all()
    response = [
        PostDtoWithVotes(post=PostDto.model_validate(post), votes=votes) for post, votes in posts
    ]

    return response

@router.get("/{id}", response_model=PostDtoWithVotes)
def get_post(id: int, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    # with psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
    #     with conn.cursor(row_factory = dict_row) as cursor:
    #         cursor.execute("""SELECT * FROM posts where id = %s""", (id,))
    #         post = cursor.fetchone()
    post_data = db.query(Post, func.count(Vote.post_id).label("votes")).outerjoin(Vote, Vote.post_id == Post.id).group_by(Post.id).order_by("votes").filter(Post.id == id).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post, votes = post_data
    
    return PostDtoWithVotes(post=post, votes=votes)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db) , token_data: TokenData = Depends(get_current_token_payload)):
    # with psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
    #     with conn.cursor(row_factory = dict_row) as cursor:
    #         cursor.execute("""DELETE FROM posts where id = %s RETURNING id""", (id,))
    #         deleted_post = cursor.fetchone()
    postQuery = db.query(Post).filter(Post.id == id)
    post = postQuery.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    only_owner_action(token_data.id, post.user_id)
    postQuery.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post successfully deleted."}

@router.put("/{id}")
def update_post(id: int, post: CreatePostRequestDto, db:Session = Depends(get_db) , token_data: TokenData = Depends(get_current_token_payload)):
    #  with psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
    #     with conn.cursor(row_factory = dict_row) as cursor:
    #         cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #         (post.title, post.content, post.published, id))
    #         update_post = cursor.fetchone()
    post_query = db.query(Post).filter(Post.id == id)
    updating_post = post_query.first()
    if not updating_post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    only_owner_action(token_data.id, updating_post.user_id)
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updating_post)
    return updating_post