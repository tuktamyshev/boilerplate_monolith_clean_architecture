from dataclasses import dataclass

from application.exceptions.base import ApplicationException


@dataclass(frozen=True)
class WrongEmailOrPasswordException(ApplicationException):
    @property
    def message(self) -> str:
        return "Wrong email or password"


@dataclass(frozen=True)
class AuthenticationException(ApplicationException):
    @property
    def message(self) -> str:
        return "Authentication failed"


@dataclass(frozen=True)
class InactiveUserException(AuthenticationException):
    @property
    def message(self) -> str:
        return "User inactive"


@dataclass(frozen=True)
class WrongTokenException(AuthenticationException):
    @property
    def message(self) -> str:
        return "Wrong token"
