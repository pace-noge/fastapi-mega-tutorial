from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.user.models import User
from config import Config
from core.utils import get_db, generate_access_token

router = APIRouter()


@router.post('/token/')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    URL for getting acces token
    :param form_data: Form data
    :param db: Sqlalchemy Session
    :return: dict of access_token
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None or not user.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})
    token_expires = timedelta(minutes=int(Config.ACCESS_TOKEN_EXPIRES_MINUTES))
    access_token = generate_access_token(data={"sub": user.username}, expires_delta=token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
