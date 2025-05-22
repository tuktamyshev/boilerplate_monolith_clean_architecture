from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordHasherInterface(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def validate_password(self, password: str, hashed_password: str) -> bool: ...
