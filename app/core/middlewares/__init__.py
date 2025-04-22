from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import CORS_ALLOWED_HEADERS, CORS_ORIGINS
from app.core.middlewares.execution_middleware import measure_execution_time


def add_middlewares(app: FastAPI) -> None:
    """
    Wrap FastAPI application, with various of middlewares
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=CORS_ALLOWED_HEADERS,
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=measure_execution_time)
