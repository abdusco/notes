from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app import database


async def db_session_middleware(request: Request, call_next: callable):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = database.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def register_middlewares(app: FastAPI):
    app.add_middleware(BaseHTTPMiddleware, dispatch=db_session_middleware)
