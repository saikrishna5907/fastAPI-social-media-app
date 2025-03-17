from typing import Literal

from pydantic import BaseModel


class VoteDTO(BaseModel):
    post_id: int
    flag: Literal[0,1]
    
    class Config:
        from_attributes = True