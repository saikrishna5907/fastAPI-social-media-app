from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String

from .base_entity import Base, BaseTimeStamp


class Vote(Base, BaseTimeStamp):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
    flag = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint('flag IN (0, 1)', name='check_flag_values'),)