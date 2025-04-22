"""Main FastAPI app instance declaration."""
import fastapi
import uvicorn

from app.core.config import settings
from app.core.middlewares import add_middlewares
from app.router import api_router

# TODO Add logger


fastapi_app = fastapi.FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=settings.OPENAPI_URL,
    docs_url=settings.DOCS_URL,
)
fastapi_app.include_router(api_router)
add_middlewares(fastapi_app)

if __name__ == "__main__":
    uvicorn.run(
        "main:fastapi_app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=True,
    )
