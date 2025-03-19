from fastapi import status
from pytest import mark

from app.schemas.post_schema import (CreatePostRequestDto, PostDto,
                                     PostDtoBase, PostDtoWithVotes)
from tests.utils import (assert_forbidden, assert_not_authenticated,
                         assert_post_not_found)

from .conftest import create_user_payload


def test_get_all_posts_no_data(authorized_client):
    response = authorized_client.get("/posts")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0
    assert data == []

def test_get_all_posts_no_data(authorized_client, test_posts):
    response = authorized_client.get("/posts")
    data = [PostDtoWithVotes.model_validate(item) for item in response.json()]
    assert response.status_code == 200
    assert len(data) == 3
    
    data.sort(key=lambda x: x.post.id)
    test_posts.sort(key=lambda x: x.id)

    # Validate post contents
    assert len(data) == len(test_posts)
    for response_post, expected_post in zip(data, test_posts):
        assert response_post.post.title == expected_post.title
        assert response_post.post.content == expected_post.content
        assert response_post.post.published == expected_post.published

def test_unauthorized_get_all_posts(test_client):
    response = test_client.get("/posts")
    assert_not_authenticated(response)
    

def test_unauthorized_get_one_post(test_client, test_posts):
    response = test_client.get(f"/posts/{test_posts[0].id}")
    assert_not_authenticated(response)

def test_get_not_exists_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{1225}")
    assert_post_not_found(response, 1225)
    
def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    data = PostDtoWithVotes.model_validate(response.json())
    
    assert response.status_code == status.HTTP_200_OK
    assert data.votes == 0
    assert data.post.title == test_posts[0].title
    assert data.post.content == test_posts[0].content
    assert data.post.published == test_posts[0].published
    assert data.post.user_id == test_posts[0].user_id
    assert data.post.id == test_posts[0].id
    assert data.post.user.email == test_posts[0].user.email
    assert data.post.user.phone == test_posts[0].user.phone
    assert data.post.user.first_name == test_posts[0].user.first_name
    assert data.post.user.last_name == test_posts[0].user.last_name
    assert data.post.user.id == test_posts[0].user.id
    
@mark.parametrize("title, content, published", [
    ("New Title 1", "New Content 1", True),
    ("New Title 2", "New Content 2", False),
    ("New Title 3", "New Content 3", True),
])
def test_get_one_post_inactive_user(authorized_client, title, content, published, test_users):
    payload = PostDtoBase(title=title, content=content, published=published)
    response = authorized_client.post(
        "/posts",
        json=payload.model_dump()
    )
    data = PostDto.model_validate(response.json())
    user = test_users[0].user
    assert response.status_code == status.HTTP_201_CREATED
    assert data.title == payload.title
    assert data.content == payload.content
    assert data.published == payload.published
    assert data.user_id == user.id
    assert data.id is not None
    assert data.created_at is not None
    assert data.user.email == user.email
    assert data.user.phone == user.phone
    assert data.user.first_name == user.first_name
    assert data.user.last_name == user.last_name
    assert data.user.id == user.id
    assert data.user.created_at is not None
    
def test_create_post_with_no_published(authorized_client, test_users):
    payload = CreatePostRequestDto(title="New Title", content="New Content")
    response = authorized_client.post(
        "/posts",
        json=payload.model_dump()
    )
    data = PostDto.model_validate(response.json())
    user = test_users[0].user
    assert response.status_code == status.HTTP_201_CREATED
    assert data.title == payload.title
    assert data.content == payload.content
    assert data.published == True
    assert data.user_id == user.id
    assert data.id is not None
    assert data.created_at is not None
    assert data.user.email == user.email
    assert data.user.phone == user.phone
    assert data.user.first_name == user.first_name
    assert data.user.last_name == user.last_name
    assert data.user.id == user.id
    assert data.user.created_at is not None


def test_unauthorized_create_post(test_client):
    payload = CreatePostRequestDto(title="New Title", content="New Content")
    response = test_client.post(
        "/posts",
        json=payload.model_dump()
    )
    assert_not_authenticated(response)
    
def test_unauthorized_delete_post(test_client, test_posts):
    response = test_client.delete(f"/posts/${test_posts[0].id}")
    assert_not_authenticated(response)

def test_delete_not_exists_post(authorized_client):
    response = authorized_client.delete(f"/posts/{1225}")
    assert_post_not_found(response, 1225)
    
def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
@mark.parametrize("test_users", [[create_user_payload, create_user_payload.model_copy(update={"email": "second_user@gmail.com"})]], indirect=True)
def test_delete_post_not_owner(authorized_client, test_users, test_posts):
    user2 = test_users[1].user
    # get post of user 2
    user2_posts = list(filter(lambda post: post.user_id == user2.id, test_posts))
    
    # try to delete post of user 2 by user 1 ( with token of user 1 i.e; not owner of post)
    response = authorized_client.delete(f"/posts/{user2_posts[0].id}")
    
    assert_forbidden(response)
    
def test_update_not_exists_post(authorized_client):
    payload = CreatePostRequestDto(title="New Title", content="New Content")
    response = authorized_client.put(
        f"/posts/{1225}",
        json=payload.model_dump()
    )
    assert_post_not_found(response, 1225)

@mark.parametrize("test_users", [[create_user_payload, create_user_payload.model_copy(update={"email": "second_user@gmail.com"})]], indirect=True)
def test_update_post_not_owner(authorized_client, test_users, test_posts):
    user2 = test_users[1].user
    # get post of user 2
    user2_posts = list(filter(lambda post: post.user_id == user2.id, test_posts))
    payload = CreatePostRequestDto(title="New Title", content="New Content")
    
    # try to update post of user 2 by user 1 ( with token of user 1 i.e; not owner of post)
    response = authorized_client.put(f"/posts/{user2_posts[0].id}", json=payload.model_dump())
    
    assert_forbidden(response)
    
def test_update_post(authorized_client, test_posts):
    payload = CreatePostRequestDto(title="Updated Title", content="Updated Content", published=False)
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json=payload.model_dump()
    )
    data = PostDtoBase.model_validate(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert data.title == payload.title
    assert data.content == payload.content
    assert data.published == False