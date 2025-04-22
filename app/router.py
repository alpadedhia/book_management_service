from fastapi import APIRouter

from app.core.config import settings

api_router = APIRouter(prefix=f"{settings.ROOT_PATH}/v1")
