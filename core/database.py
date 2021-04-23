"""
This script intended to used as main configuration to connect to database using sqlalchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

# connect_args={"check_same_thread": False"} <- this is only for sqlite db
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
