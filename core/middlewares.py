"""
Middleware for our apps that will be intercept the request and response before executed by our own code
"""
from fastapi import Request, Response
from app import app
from core.database import SessionLocal


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Inject the database session into request state, before we continue
    :param request: FastAPI Request
    :param call_next: next call
    :return: FastAPI Response
    """
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
