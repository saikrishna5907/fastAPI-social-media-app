from sqlalchemy import TIMESTAMP, Column, text

from app.config.database import Base


class BaseTimeStamp:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
