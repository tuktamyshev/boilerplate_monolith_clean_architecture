from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.value_objects.email import EmailValueObject


@dataclass(frozen=True)
class EmailServiceInterface(ABC):
    @abstractmethod
    async def send_verification_to_email(self, email: EmailValueObject) -> None: ...

    @abstractmethod
    def verify_email(self, token: str) -> str: ...
