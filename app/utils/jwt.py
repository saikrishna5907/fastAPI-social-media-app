import os
from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..database import get_db
from ..entities.user_entity import User
from ..schemas.token_schema import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_SECRET_KEY_EXPIRE_MINUTES = int(os.getenv("JWT_SECRET_KEY_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(token_data: TokenData, expires_delta: Union[timedelta, None] = JWT_SECRET_KEY_EXPIRE_MINUTES):
    to_encode = token_data.model_dump()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("email")
        id: str = payload.get("id")
        if id is None or email is None:
            raise credentials_exception
    except jwt.PyJWTError as e:
        print(e)
        raise credentials_exception

    return TokenData(email=email, id=id)

def get_current_token_payload(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"})
    
    return  verify_access_token(token, credentials_exception)

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"})
    
    token:TokenData =  verify_access_token(token, credentials_exception)
    if token.id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == token.id).first()
    if user is None:
        raise credentials_exception
    return user