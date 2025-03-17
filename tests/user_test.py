from app.schemas.user_schema import CreateUserRequestDto, UserDto

from .test_db import test_client

create_user_payload = CreateUserRequestDto(
    email= "sai23@gmail.com",
            password= "test123",
            phone= "+447824603561",
            first_name= "Saikrishna",
            last_name= "Sangishetty"
)


def test_create_user(test_client):
    response = test_client.post(
        "/users",
        json=create_user_payload.model_dump()
    )
    data = UserDto.model_validate(response.json())
    assert response.status_code == 201
    assert data.email == create_user_payload.email
    assert data.phone == create_user_payload.phone
    assert data.first_name == create_user_payload.first_name
    assert data.last_name == create_user_payload.last_name
    assert data.id is not None
    assert data.created_at is not None  