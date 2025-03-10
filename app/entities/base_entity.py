from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, text)
from sqlalchemy.orm import relationship


class BaseTimeStamp:
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
