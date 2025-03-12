from sqlalchemy import TIMESTAMP, Column, text

from ..database import Base


class BaseTimeStamp:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
