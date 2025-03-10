from datetime import datetime

from pydantic import BaseModel, EmailStr

from .base_schema import CreateAtBaseModel
from .user_schema import UserDto


class PostDtoBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePostRequestDto(PostDtoBase):
    pass

class PostDto(PostDtoBase, CreateAtBaseModel):
    pass
    id: int
    user_id: int
    user: UserDto
