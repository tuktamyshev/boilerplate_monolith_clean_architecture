import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from faststream import ExceptionMiddleware
from faststream.asyncapi.proto import AsyncAPIApplication
from starlette import status
from starlette.responses import Response
from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult

from application.exceptions.auth import AuthenticationException
from application.exceptions.base import ApplicationException
from domain.exceptions.base import DomainException

logger = logging.getLogger("webserver")


def init_exceptions_handlers(app: FastAPI) -> None:
    init_fastapi_exception_handlers(app)
    init_faststream_exception_handlers(app.state.faststream_app)


def init_fastapi_exception_handlers(app: FastAPI) -> None:
    # Handler for expected server errors
    @app.exception_handler(DomainException)
    @app.exception_handler(ApplicationException)
    @app.exception_handler(HTTPException)
    async def application_exception_handler(request: Request, exc: DomainException | ApplicationException) -> Response:
        if isinstance(exc, AuthenticationException):
            http_exc = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=exc.message,
            )
        else:
            http_exc = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=exc.message,
            )

        return await http_exception_handler(request, http_exc)

    # Handler for unexpected server errors
    @app.exception_handler(Exception)
    async def internal_server_error_handler(request: Request, exc: Exception) -> Response:
        logger.exception(f"{request.url}: {exc}")
        http_exc = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
        return await http_exception_handler(request, http_exc)


faststream_exc_middleware = ExceptionMiddleware()


def init_faststream_exception_handlers(app: AsyncAPIApplication) -> None:
    # Handler for expected server errors
    @faststream_exc_middleware.add_handler(DomainException)
    @faststream_exc_middleware.add_handler(ApplicationException)
    async def application_error_handler(exc: DomainException | ApplicationException) -> None:
        raise exc

    # Handler for unexpected server errors
    @faststream_exc_middleware.add_handler(Exception)
    async def internal_server_error_handler(exc: Exception) -> None:
        logger.exception(str(exc))
        raise exc


class ExceptionLoggingMiddleware(TaskiqMiddleware):
    def post_save(self, message: "TaskiqMessage", result: "TaskiqResult[Any]") -> None:
        if result.is_err:
            try:
                raise result.error
            except Exception as ex:
                logger.exception(ex)
