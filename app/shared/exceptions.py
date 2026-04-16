class BigBossException(Exception):
    status_code: int = 500
    error_type: str = "internal-error"
    title: str = "Internal Server Error"
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str = "") -> None:
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class NotFoundException(BigBossException):
    status_code = 404
    error_type = "not-found"
    title = "Not Found"


class ConflictException(BigBossException):
    status_code = 409
    error_type = "conflict"
    title = "Conflict"


class ForbiddenException(BigBossException):
    status_code = 403
    error_type = "forbidden"
    title = "Forbidden"


class UnauthorizedException(BigBossException):
    status_code = 401
    error_type = "unauthorized"
    title = "Unauthorized"


class ValidationException(BigBossException):
    status_code = 422
    error_type = "validation-error"
    title = "Validation Error"
