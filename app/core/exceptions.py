class AppError(Exception):
    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = 404
    detail = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    detail = "Resource already exists"


class InvalidCredentialsError(AppError):
    status_code = 401
    detail = "Invalid credentials"


class UnauthorizedError(AppError):
    status_code = 401
    detail = "Not authenticated"
