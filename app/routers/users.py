from fastapi import APIRouter, Depends, status, HTTPException
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


@router.get("{user_id}/", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    """
    Get User detail
    :param user_id: int user id
    :param db: Sqlalachemy db Session
    :return: User Model
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.put("{user_id}", response_model=UserSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Update user detail
    :param user_id: int user id in url parameter
    :param user: user json
    :param db:
    :return:
    """
    current_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    current_user.username = user.username
    current_user.email = user.email
    db.commit()
    db.refresh(current_user)
    return current_user
    return current_user
