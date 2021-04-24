"""
Utility or helper for our app
"""
from fastapi import Request


def get_db(request: Request):
    return request.state.db
