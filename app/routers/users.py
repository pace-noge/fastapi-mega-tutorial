from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.models import User as UserModel
from app.schemas import User as UserSchema, UserCreate
from core.utils import get_db

router = APIRouter()


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserModel(username=user.username, email=user.email)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[UserSchema], status_code=status.HTTP_200_OK)
async def user_list(db: Session = Depends(get_db)):
    """
    GET list of users
    :param db: Sqlalchemy.orm Session
    :return: QuerySet of User models
    """
    users = db.query(UserModel).all()
    return users
