from starlette import status


class BaseError(Exception):
    status_code: int
    code: int
    title: str
    default_detail: str
    content: dict

    def __init__(self, detail: str = None):
        self.detail = detail or self.default_detail
        self.content = {
            "code": self.code,
            "title": self.title,
            "detail": self.detail,
        }


class BadRequestError(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = 400
    title = "Bad Request"
    default_detail = "The server cannot process the request from the client"


class ForbiddenError(BaseError):
    status_code = status.HTTP_403_FORBIDDEN
    code = 403
    title = "Forbidden"
    default_detail = "Forbidden"


class UnauthorizedError(BaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = 401
    title = "Unauthorized"
    default_detail = "Unauthorized"


class NotFoundError(BaseError):
    status_code = status.HTTP_404_NOT_FOUND
    code = 404
    title = "Not Found"
    default_detail = "Not Found"


class ConflictError(BaseError):
    status_code = status.HTTP_409_CONFLICT
    code = 409
    title = "Conflict"
    default_detail = "Conflict"


class UnprocessableEntity(BaseError):
    status_code = status.HTTP_409_CONFLICT
    code = 422
    title = "Unprocessable Entity"
    default_detail = "Unprocessable Entity"


class ConnectionException(BaseError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = 500
    title = "Could not initialise connection"
    default_detail = "The connection could not be established"
