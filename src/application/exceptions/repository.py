from dataclasses import dataclass
from uuid import UUID

from application.exceptions.base import ApplicationException


@dataclass(frozen=True)
class ModelDoesNotExists(ApplicationException):
    uuid: UUID

    @property
    def message(self) -> str:
        return f"Model does not exists: {self.uuid}"
