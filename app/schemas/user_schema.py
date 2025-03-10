
from datetime import datetime

from pydantic import BaseModel, EmailStr

from .base_schema import CreateAtBaseModel


class UserLoginRequestDto(BaseModel):
        email: EmailStr
        password: str

class CreateUserRequestDto(BaseModel):
    email: EmailStr
    password: str

class UserDtoBase(CreateAtBaseModel):
    email: EmailStr
    id: int

class UserDto(UserDtoBase):
    pass