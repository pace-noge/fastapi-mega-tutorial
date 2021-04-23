from datetime import timedelta

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import app, models, schemas
from core.utils import generate_access_token, oauth2_scheme
from config import Config


def get_db(request: Request):
    return request.state.db


@app.get("/")
@app.get("/index")
def home_page():
    return {"message": "Hello world"}


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if user is None or not user.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"})
    token_expires = timedelta(minutes=int(Config.ACCESS_TOKEN_EXPIRES_MINUTES))
    access_token = generate_access_token(data={"sub": user.username}, expires_delta=token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
