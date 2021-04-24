from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from core.database import Base

from app.post.models import Post

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    is_active = Column(Boolean, default=False)
    posts = relationship('Post', back_populates='author')

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __str__(self):
        return f"<User {self.username}>"