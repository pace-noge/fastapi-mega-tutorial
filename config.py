import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'm5sHiNkgRll07uumdGS3ZCbd1FxZqad16pvQCySAxCs'
    ALGORITHM = os.environ.get("ALGORITHM") or "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRES_MINUTES") or 15
