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

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    """
    Not much change from BaseModel
    But for sake readibility we add PostCreate
    """
    pass


class Post(PostBase):
    """
    this is for post representation
    """
    id:  int
    author_id: int
