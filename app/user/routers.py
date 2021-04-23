import fastapi
from sqlalchemy.orm import Session
from typing import List

from .models import User as UserModel
from .schemas import User as UserSchema, UserCreate, UserBase, ResetPassword
from core.utils import get_db

router = fastapi.APIRouter()


@router.post("/", response_model=UserSchema, status_code=fastapi.status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = fastapi.Depends(get_db)):
    new_user = UserModel(username=user.username, email=user.email)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[UserSchema], status_code=fastapi.status.HTTP_200_OK)
async def user_list(db: Session = fastapi.Depends(get_db)):
    """
    GET list of user
    :param db: Sqlalchemy.orm Session
    :return: QuerySet of User models
    """
    users = db.query(UserModel).all()
    return users


@router.get("/{user_id}", response_model=UserSchema, status_code=fastapi.status.HTTP_200_OK)
async def user_detail(user_id: int, db: Session = fastapi.Depends(get_db)):
    """
    Get User detail
    :param user_id: int user id
    :param db: Sqlalachemy db Session
    :return: User Model
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.put("/{user_id}", response_model=UserSchema, status_code=fastapi.status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserBase, db: Session = fastapi.Depends(get_db)):
    """
    Update user detail
    :param user_id: int user id in url parameter
    :param user: user json
    :param db:
    :return:
    """
    current_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not current_user:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found.")
    current_user.username = user.username
    current_user.email = user.email
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/{user_id}/reset-password", status_code=fastapi.status.HTTP_200_OK)
async def change_password(user_id: int, data: ResetPassword, db: Session = fastapi.Depends(get_db)):
    current_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not current_user:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"User not found.")
    if current_user.verify_password(data.current_password):
        current_user.set_password(data.new_password)
        db.commit()
        db.refresh(current_user)
        return {"message": "password updated"}
    raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="invalid current password")