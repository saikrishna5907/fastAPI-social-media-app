
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.utils.custom_exceptions import NotFoundException

from ..config.database import get_db
from ..entities.user_entity import User
from ..schemas.user_schema import CreateUserRequestDto, UserDto
from ..utils.jwt import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserDto)
def create_user(user: CreateUserRequestDto, db:Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserDto)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise NotFoundException(detail=f"No user found with id: {id}")
    return user