from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    body = Column(String(140))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow())
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates="posts")

    def __str__(self):
        return f"<Post {self.body[30:]}>"
