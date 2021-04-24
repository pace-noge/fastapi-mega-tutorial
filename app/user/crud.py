from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import schemas
from . import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, data: schemas.UserCreate):
    if data.password != data.password1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password not same")
    user = models.User(username=data.username, email=data.email)
    user.set_password(data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, data: schemas.UserBase, user: models.User):
    user.username = data.username
    user.email = data.email
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
    return True


def update_password(db: Session, instance: models.User, data: schemas.ChangePassword):
    if instance.verify_password(data.current_password):
        instance.set_password(data.new_password)
        return True
    return False
