
from fastapi import status
from pytest import mark

from app.entities.post_entity import Post
from app.schemas.vote_schema import VoteDTO
from tests.utils import (assert_not_authenticated, assert_post_not_found,
                         assert_vote_create_success,
                         assert_vote_update_success)

from .conftest import create_user_payload, vote_payload

votePayload = VoteDTO(
    post_id=1,
    flag=0
)


def test_not_found_post_vote(authorized_client):
    response = authorized_client.post(
        "/vote",
        json=votePayload.model_copy(update={"post_id": 100}).model_dump()
    )
    assert_post_not_found(response, 100)
    
def test_create_new_vote_on_own_post(create_vote_own_post):
    assert_vote_create_success(create_vote_own_post)
    
@mark.parametrize("test_users", [[create_user_payload, create_user_payload.model_copy(update={"email": "second_user@gmail.com"})]], indirect=True)
def test_create_new_vote_on_another_user_post(create_new_vote_on_another_user_post):
    assert_vote_create_success(create_new_vote_on_another_user_post)

def test_duplicate_vote_on_own_post(authorized_client, create_vote_own_post):
    payload = vote_payload(1)
    
    duplicateVoteResponse = authorized_client.post("/vote",json=payload.model_dump())
    
    assert duplicateVoteResponse.json()["detail"] == "You have already un voted on post 1"
    assert duplicateVoteResponse.status_code == status.HTTP_409_CONFLICT
    
@mark.parametrize(
    "test_users, create_new_vote_on_another_user_post", [
        ([create_user_payload, create_user_payload.model_copy(update={"email": "second_user@gmail.com"})], 1)
    ], 
    indirect=True)
def test_duplicate_vote_on_another_user_post(authorized_client,  test_users, create_new_vote_on_another_user_post,test_db_session):
    user2 = test_users[1].user
    user2_posts = test_db_session.query(Post).filter(Post.user_id == user2.id).all()
    payload = vote_payload(user2_posts[0].id, 1)
    
    duplicateVoteResponse = authorized_client.post("/vote",json=payload.model_dump())
    
    assert duplicateVoteResponse.json()["detail"] == "You have already voted on post 4"
    assert duplicateVoteResponse.status_code == status.HTTP_409_CONFLICT

@mark.parametrize(
    "test_users, create_new_vote_on_another_user_post", [
        ([create_user_payload, create_user_payload.model_copy(update={"email": "second_user@gmail.com"})], 1)
    ], 
    indirect=True)
def test_update_vote_on_own_post(authorized_client, create_new_vote_on_another_user_post, test_users, test_db_session):
    user2 = test_users[1].user
    user2_posts = test_db_session.query(Post).filter(Post.user_id == user2.id).all()
    
    payload = vote_payload(user2_posts[0].id, 0)
    
    response = authorized_client.post("/vote",json=payload.model_dump())
    
    assert_vote_update_success(response)
    
@mark.parametrize(
    "test_users, create_vote_own_post", [
        ([create_user_payload, create_user_payload.model_copy(update={"email": "second_user@gmail.com"})], 0)
    ], 
    indirect=True)
def test_update_vote_on_own_post(authorized_client, create_vote_own_post, test_users, test_db_session):
    user = test_users[0].user
    user_posts = test_db_session.query(Post).filter(Post.user_id == user.id).all()
    
    payload = vote_payload(user_posts[0].id, 1)
    
    response = authorized_client.post("/vote",json=payload.model_dump())
    
    assert_vote_update_success(response)

def test_unauthorized_vote(test_client):
    response = test_client.post("/vote",json=votePayload.model_dump())
    
    assert_not_authenticated(response)