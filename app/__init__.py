from fastapi import FastAPI

from . import models, schemas
from .routers import authentications, main, users
from core.database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Micro Blog")
from core import middlewares

app.include_router(authentications.router, prefix="/auth", tags=["auth"])
app.include_router(main.router)
app.include_router(users.router, prefix="/users", tags=["users"])
