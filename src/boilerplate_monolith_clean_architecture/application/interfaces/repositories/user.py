from abc import ABC
from dataclasses import dataclass

from application.interfaces.repositories.base import BaseRepository
from domain.entities.user import UserEntity
from domain.value_objects.email import EmailValueObject


@dataclass(frozen=True)
class UserRepository(BaseRepository[UserEntity], ABC):
    async def delete_by_email(self, email: EmailValueObject) -> None: ...
