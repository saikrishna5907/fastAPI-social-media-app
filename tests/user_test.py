from fastapi import status
from pytest import fixture

from app.entities.user_entity import User
from app.schemas.user_schema import UserDto

from .conftest import create_user_payload


def test_get_user(test_user, test_client):
    response = test_client.get("/users/1")
    userDetails = UserDto.model_validate(response.json())
    data = test_user[0]
    assert response.status_code == status.HTTP_200_OK
    assert userDetails.email == data.email
    assert userDetails.phone == data.phone
    assert userDetails.first_name == data.first_name
    assert userDetails.last_name == data.last_name
    assert userDetails.id == 1
    assert userDetails.created_at is not None
    
def test_get_user_not_found(test_client):
    response = test_client.get("/users/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No user found with id: 1"
    

def test_create_user(test_user):
    data, status_code = test_user
    assert status_code == status.HTTP_201_CREATED
    assert data.email == create_user_payload.email
    assert data.phone == create_user_payload.phone
    assert data.first_name == create_user_payload.first_name
    assert data.last_name == create_user_payload.last_name
    assert data.id is not None
    assert data.created_at is not None  