from pydantic import BaseModel, EmailStr

from .base_schema import CreateAtBaseModel


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
    id: int
    class Config:
        from_attributes = True

class UserDto(UserDtoBase):
    pass