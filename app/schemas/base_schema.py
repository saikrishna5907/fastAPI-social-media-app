from datetime import datetime

from pydantic import BaseModel


class CreateAtBaseModel(BaseModel):
    created_at: datetime