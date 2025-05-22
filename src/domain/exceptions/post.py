from dataclasses import dataclass
from uuid import UUID

from domain.exceptions.base import DomainException


@dataclass(frozen=True)
class PostDoesNotExistsException(DomainException):
    uuid: UUID

    @property
    def message(self) -> str:
        return f"Post does not exists: {self.uuid}"


@dataclass(frozen=True)
class PostTextCannotBeEmptyException(DomainException):
    @property
    def message(self) -> str:
        return "Post text cannot be empty"


@dataclass(frozen=True)
class PostTextTooLongException(DomainException):
    length: int
    max_len: int

    @property
    def message(self) -> str:
        return f"Post text too long: max_len={self.max_len}, length={self.length} symbols"
