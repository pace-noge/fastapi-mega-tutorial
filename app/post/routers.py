from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.utils import get_db
from core.security import get_current_user
from .crud import create_post
from .schemas import Post, PostCreate
from app.user.models import User as UserModel

router = APIRouter()


@router.post("/", response_model=Post)
async def new_post(data: PostCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_post = create_post(db, data, current_user)
    return new_post
