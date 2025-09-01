from sqlalchemy import Boolean, Column, Integer, String, text

from app.entities.base_entity import Base, BaseTimeStamp


class User(Base, BaseTimeStamp):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    active = Column(Boolean, default=True, server_default=text("true"))
    
    