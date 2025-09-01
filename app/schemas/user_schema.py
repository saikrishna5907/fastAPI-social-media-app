from pydantic import BaseModel, EmailStr

from app.schemas.base_schema import CreateAtBaseModel


class UserLoginRequestDto(BaseModel):
        email: EmailStr
        password: str

class CreateUserRequestDto(BaseModel):
    email: EmailStr
    password: str
    phone: str
    first_name: str
    last_name: str
    active: bool = True

class UserDtoBase(CreateAtBaseModel):
    email: EmailStr
    phone: str
    first_name: str
    last_name: str
    id: int
    class Config:
        from_attributes = True

class UserDto(UserDtoBase):
    pass