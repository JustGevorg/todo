from typing import Callable, Awaitable, Iterable
from starlette.requests import Request
from fastapi.responses import JSONResponse
from dataclasses import dataclass
from fastapi import status, FastAPI

from exceptions.exceptions import BaseTodoException, TaskAlreadyExists, TaskNotExistsException

ExceptionHandler = Callable[[Request, BaseTodoException], Awaitable[JSONResponse]]


@dataclass
class ExceptionWithStatusCodeAndHandler:
    """
    Связка исключения с кодом ошибки HTTP и обработчиком этой ошибки
    """
    exception_type: type(BaseTodoException)
    status_sode: int
    __exception_handler: ExceptionHandler = None

    def __post_init__(self):
        self.__exception_handler = exception_handler_factory(self.status_sode)

    @property
    def exception_handler(self):
        return self.__exception_handler


def exception_handler_factory(status_code: int) -> ExceptionHandler:
    """
    Фабрика exception_handler-ов для приложения FastAPI
    :param status_code: Числовой код статуса
    :return: Обработчик исключения с полученным из исключения description
    """

    async def exception_handler(_: Request, exc: BaseTodoException):
        return JSONResponse(
            status_code=status_code,
            content={"detail": exc.description}
        )

    return exception_handler


def add_exception_handlers(app: FastAPI,
                           exceptions_with_handlers: Iterable[ExceptionWithStatusCodeAndHandler]) -> FastAPI:
    """
    Регистрация обработчиков ошибок для приложения FastAPI
    :param app: объект приложения FastAPI
    :param exceptions_with_handlers: связка типа ошибки и обработчика
    :return:
    """
    for pair in exceptions_with_handlers:
        app.add_exception_handler(pair.exception_type, pair.exception_handler)  # noqa typing

    return app


EXCEPTION_HANDLERS = [
    ExceptionWithStatusCodeAndHandler(TaskAlreadyExists, status.HTTP_409_CONFLICT),
    ExceptionWithStatusCodeAndHandler(TaskNotExistsException, status.HTTP_404_NOT_FOUND),
]
