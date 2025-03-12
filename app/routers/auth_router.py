from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..entities.user_entity import User
from ..schemas.token_schema import Token, TokenData
from ..utils.jwt import create_access_token, verify_password

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    invalid_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    user = db.query(User).filter(User.email == login_data.username).first()
    if not user or not user.active:
        invalid_exception
    if not login_data.password or not user.password:
        invalid_exception
    if not verify_password(login_data.password, user.password):
        invalid_exception

    access_token = create_access_token(
      TokenData(email=user.email, id=user.id)
    )
    
    return Token(access_token=access_token, token_type="bearer")
