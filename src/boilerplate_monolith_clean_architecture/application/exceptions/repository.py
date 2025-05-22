from dataclasses import dataclass

from application.exceptions.base import ApplicationException


@dataclass(frozen=True)
class ModelDoesNotExists(ApplicationException):
    @property
    def message(self) -> str:
        return "Model does not exists"
