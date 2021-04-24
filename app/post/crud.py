from sqlalchemy.orm import Session
from .schemas import PostCreate
from .models import Post
from app.user.models import User


def create_post(db: Session, data: PostCreate, author: User):
    new_post = Post(body=data.body, author_id=author.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
