from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base
from .base_entity import BaseTimeStamp


class User(Base, BaseTimeStamp):
    __tablename__ = "users"
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True, nullable=False)