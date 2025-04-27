from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions.base_exception import (
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    UnprocessableEntity,
)
from app.main import fastapi_app


@fastapi_app.exception_handler(ForbiddenError)
async def forbidden_error_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )


@fastapi_app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )


@fastapi_app.exception_handler(UnauthorizedError)
async def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )


@fastapi_app.exception_handler(UnprocessableEntity)
async def unprocessable_entity_error_handler(
    request: Request, exc: UnprocessableEntity
):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )
