from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(frozen=True)
class AccessException(DomainException):
    @property
    def message(self) -> str:
        return "Access denied"
