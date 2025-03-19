from fastapi import status
from pytest import fixture

from app.entities.user_entity import User
from app.schemas.user_schema import UserDto

from .conftest import create_user_payload


def test_get_user(test_users, test_client):
    response = test_client.get("/users/1")
    userDetails = UserDto.model_validate(response.json())
    user = test_users[0].user
    assert response.status_code == status.HTTP_200_OK
    assert userDetails.email == user.email
    assert userDetails.phone == user.phone
    assert userDetails.first_name == user.first_name
    assert userDetails.last_name == user.last_name
    assert userDetails.id == 1
    assert userDetails.created_at is not None
    
def test_get_user_not_found(test_client):
    response = test_client.get("/users/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No user found with id: 1"
    

def test_create_user(test_users):
    user = test_users[0].user
    code = test_users[0].status_code
    assert code == status.HTTP_201_CREATED
    assert user.email == create_user_payload.email
    assert user.phone == create_user_payload.phone
    assert user.first_name == create_user_payload.first_name
    assert user.last_name == create_user_payload.last_name
    assert user.id is not None
    assert user.created_at is not None  