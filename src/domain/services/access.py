from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.entities.user import UserEntity
from domain.exceptions.access import AccessException


# TODO remake this horror into something normal is you need more complex behavior https://www.youtube.com/watch?v=5GG-VUvruzE&list=LL&index=12&t=30s
@dataclass(frozen=True)
class AccessService:
    def check_is_admin(self, user: UserEntity) -> None:
        if user.is_superuser:
            return
        raise AccessException()

    def check_is_owner(self, user_uuid: UUID, entity: BaseEntity) -> None:
        if entity.user_uuid == user_uuid:
            return
        raise AccessException()
