from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateAtBaseModel(BaseModel):
    created_at: datetime