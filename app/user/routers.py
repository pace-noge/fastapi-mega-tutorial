import fastapi
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from .models import User as UserModel
from .schemas import User as UserSchema, UserCreate, UserBase, ChangePassword
from . import crud
from core.utils import get_db, get_current_user

router = fastapi.APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/")


@router.post("/", response_model=UserSchema, status_code=fastapi.status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = fastapi.Depends(get_db)):
    """
    Create new user
    :param user: User schema (post body)
    :param db: Session
    :return: new user model
    """
    new_user = crud.create_user(db, user)
    return new_user


@router.get("/", response_model=List[UserSchema], status_code=fastapi.status.HTTP_200_OK)
async def user_list(db: Session = fastapi.Depends(get_db), skip: int = 0, limit: int = 0, current_user: UserModel = fastapi.Depends(get_current_user)):
    """
    GET list of user
    :param current_user: current user based on token
    :param limit: Max user returned
    :param skip: offset user in table
    :param db: Sqlalchemy.orm Session
    :return: QuerySet of User models
    """

    if not current_user:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access.")
    users = crud.get_users(db, skip, limit)
    return users


@router.get("/{user_id}/", response_model=UserSchema, status_code=fastapi.status.HTTP_200_OK)
async def user_detail(user_id: int, db: Session = fastapi.Depends(get_db)):
    """
    Get User detail
    :param user_id: int user id
    :param db: Sqlalachemy db Session
    :return: User Model
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.put("/{user_id}/", response_model=UserSchema, status_code=fastapi.status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserBase, db: Session = fastapi.Depends(get_db)):
    """
    Update user detail
    :param user_id: int user id in url parameter
    :param user: user json
    :param db:
    :return:
    """
    current_user = crud.get_user(db, user_id)
    if not current_user:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="User not found.")
    updated_user = crud.update_user(db, user)
    return updated_user


@router.post("/{user_id}/reset-password/", status_code=fastapi.status.HTTP_200_OK)
async def change_password(user_id: int, data: ChangePassword, db: Session = fastapi.Depends(get_db)):
    """
    Update password for user
    :param user_id: int user id
    :param data: ChangePassword Schema
    :param db: Session
    :return: dict
    """
    current_user = crud.get_user(db, user_id)
    if not current_user:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"User not found.")
    password_changed = crud.update_password(db, current_user, data)
    if password_changed:
        return {"message": "password updated"}
    raise fastapi.HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail="invalid current password")