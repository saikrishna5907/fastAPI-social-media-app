from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from .base_entity import Base, BaseTimeStamp


class Post(Base, BaseTimeStamp):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, server_default=text("true"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")
    