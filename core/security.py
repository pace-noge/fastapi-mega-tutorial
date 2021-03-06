from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.schemas import TokenData
from app.user.models import User
from config import Config
from .utils import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/")


def generate_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generate access token for user
    :param data:
    :param expires_delta: expires time in minutes
    :return: encoded jwt token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Get current user based on token
    :param db:  Sqlalchemy Session
    :param token: str token
    :return: User models
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
        headers={"www-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Get current user status
    :param current_user: User Models
    :return: HTTP Bad Request or User Models
    """
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User")
    return current_user
