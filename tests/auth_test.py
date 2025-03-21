from fastapi import status
from pytest import mark

from app.schemas.token_schema import Token
from app.utils.jwt import get_current_token_payload

from .conftest import create_user_payload

inactive_user_payload = create_user_payload.model_copy(update={"active": False})

def test_login(test_users, test_client):
    user = test_users[0].user
    response = test_client.post(
        "/login",
        data={"username": user.email, "password": create_user_payload.password}
    )
    data = Token.model_validate(response.json())
    token_data = get_current_token_payload(data.access_token)
    assert response.status_code == status.HTTP_200_OK
    assert data.token_type == "bearer"
    assert data.access_token is not None
    assert data.access_token != ""
    assert token_data.email == user.email
    assert token_data.id == test_users[0].user.id
    
def test_login_with_no_user_found(test_client):
    response = test_client.post(
        "/login",
        data={"username": "test@notfound.com", "password": "123456"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Invalid Credentials"

def test_login_with_user_wrong_password(test_client, test_users):
    user = test_users[0].user
    response = test_client.post(
        "/login",
        data={"username": user.email, "password": "123456"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Invalid Credentials"

@mark.parametrize("test_users", [[inactive_user_payload]], indirect=True)
def test_login_with_inactive_user(test_client, test_users):
    user = test_users[0].user
    response = test_client.post(
        "/login",
        data={"username": user.email, "password": "123456"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Invalid Credentials"
    
def test_login_with_password_in_payload(test_client, test_users):
    user = test_users[0].user
    response = test_client.post(
        "/login",
        data={"username": user.email, "password": None}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Invalid Credentials"