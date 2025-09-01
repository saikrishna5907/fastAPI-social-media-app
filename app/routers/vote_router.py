from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.entities.post_entity import Post
from app.entities.vote_entity import Vote
from app.schemas.token_schema import TokenData
from app.schemas.vote_schema import VoteDTO
from app.utils.custom_exceptions import ConflictException, NotFoundException
from app.utils.jwt import get_current_token_payload

router = APIRouter(
    prefix="/vote",
    tags=["vote"],    
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(data: VoteDTO, db:Session = Depends(get_db), token_payload: TokenData = Depends(get_current_token_payload)):

    # Check if post exists
    post = db.query(Post).filter(Post.id == data.post_id).first()

    if not post:
        raise NotFoundException(detail=f"Post with id: {data.post_id} was not found")

    vote_query =  db.query(Vote).filter(Vote.post_id == data.post_id, Vote.user_id == token_payload.id)
    vote = vote_query.first()
    already_voted_message = f"You have already voted on post {data.post_id}"
    already_un_voted_message = f"You have already un voted on post {data.post_id}"
    
    # Check if the user has already voted
    if vote:
        # Check if the user is trying to duplicate the vote
        if data.flag == vote.flag:
            # If the user is trying to duplicate the vote then raise an error
            if vote.flag == 1:
                raise ConflictException(detail=already_voted_message)
            else:
                raise ConflictException(detail=already_un_voted_message)
            
        # If the user is not trying to duplicate the vote then update the existing vote
        else:
            # If the user is updating the existing vote
            vote.flag = data.flag
            db.commit()
            return {"message": "Vote updated successfully"}
        
    # If the user has not voted then create a new vote
    else:
        new_vote = Vote(post_id=data.post_id, user_id=token_payload.id, flag=data.flag)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
        
            