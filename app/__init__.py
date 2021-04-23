from fastapi import FastAPI
from .user.routers import router as user_router
from .auth.routers import router as auth_router
from .home_page.routers import router as home_page_router
from .post.models import Post
from .user.models import User

from core.database import engine, Base

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Micro Blog")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(home_page_router)
app.include_router(user_router, prefix="/users", tags=["user"])
