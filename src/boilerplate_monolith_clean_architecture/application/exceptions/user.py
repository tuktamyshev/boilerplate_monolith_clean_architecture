from dataclasses import dataclass

from application.exceptions.base import ApplicationException


@dataclass(frozen=True)
class UserWithThisEmailAlreadyExistsException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"User with this email already exists: {self.email}"


@dataclass(frozen=True)
class UserWithThisEmailDoesNotExistsException(ApplicationException):
    email: str

    @property
    def message(self) -> str:
        return f"User with this email does not exists: {self.email}"
