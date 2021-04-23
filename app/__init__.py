from fastapi import FastAPI

from . import models, schemas
from core.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Micro Blog")

from app import routes
