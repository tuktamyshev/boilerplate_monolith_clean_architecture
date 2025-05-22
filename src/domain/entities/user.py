from datetime import datetime
from uuid import UUID, uuid4

from domain.entities.base import BaseEntity
from domain.value_objects.email import EmailValueObject


class UserEntity(BaseEntity):
    uuid: UUID
    email: EmailValueObject
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    @classmethod
    def create(cls, email: EmailValueObject, hashed_password: str) -> "UserEntity":
        return cls(
            uuid=uuid4(),
            created_at=datetime.now(),
            email=email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
