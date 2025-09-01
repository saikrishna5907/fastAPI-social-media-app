from pydantic import BaseModel

from app.schemas.base_schema import CreateAtBaseModel
from app.schemas.user_schema import UserDto


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
    class Config:
        from_attributes = True
    

class PostDtoWithVotes(BaseModel):
    post: PostDto
    votes: int
    class Config:
        from_attributes = True
