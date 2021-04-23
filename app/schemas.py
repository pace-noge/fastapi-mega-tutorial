"""
Schema for request and response.
You can threat this file like serializers.py when using django rest
"""

from typing import List, Optional
from pydantic import BaseModel


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
