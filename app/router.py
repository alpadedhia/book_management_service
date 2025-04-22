from fastapi import APIRouter

from app.api.books import router as books_router
from app.core.config import settings

api_router = APIRouter(prefix=f"{settings.ROOT_PATH}/v1")
api_router.include_router(books_router)
