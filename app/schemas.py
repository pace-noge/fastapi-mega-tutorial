from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base models  for user
    """
    username: str
    email: str


class UserCreate(UserBase):
    """
    When create new user password must be supplied.
    """
    password: str


class User(UserBase):
    """
    When display or get the user we need to include the id
    but without password
    """
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    """"
    BaseModel for Posts
    """
    body: str
    timestamp: str
    author: str


class PostCreate(BaseModel):
    """
    Not much change from BaseModel
    But for sake readibility we add PostCreate
    """
    pass


class Token(BaseModel):
    acces_token: str
    token_type: str


class TokenData(Token):
    username: Optional[str] = None
