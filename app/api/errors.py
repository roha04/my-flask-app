from collections.abc import Callable
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.exceptions import (
    ConflictError,
    NotFoundError,
    ServiceError,
    UnauthorizedError,
    ValidationError,
)


def service_error_handler(status_code: int) -> Callable[[Request, ServiceError], JSONResponse]:
    def handler(_request: Request, exc: ServiceError) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    return handler


SERVICE_ERROR_HANDLERS: dict[type[ServiceError], Callable[[Request, Any], JSONResponse]] = {
    NotFoundError: service_error_handler(404),
    ConflictError: service_error_handler(409),
    UnauthorizedError: service_error_handler(401),
    ValidationError: service_error_handler(422),
}


def register_exception_handlers(app) -> None:
    for exc_class, handler in SERVICE_ERROR_HANDLERS.items():
        app.add_exception_handler(exc_class, handler)
