from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(frozen=True)
class InvalidEmailException(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f"Invalid email: {self.email}"


@dataclass(frozen=True)
class EmailMustBeLowercaseException(DomainException):
    email: str

    @property
    def message(self) -> str:
        return f"Email must be lowercase: {self.email}"


@dataclass(frozen=True)
class EmailTooLongException(DomainException):
    length: int
    max_len: int

    @property
    def message(self) -> str:
        return f"Email too long: max_len={self.max_len}, length={self.length} symbols"
