from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from adapters.orm.base import BaseORM
from adapters.orm.post import PostORM
from domain.value_objects.email import EmailValueObject


class UserORM(BaseORM):
    email: Mapped[EmailValueObject] = mapped_column(String(), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    is_active: Mapped[bool]
    is_superuser: Mapped[bool]
    is_verified: Mapped[bool]

    posts: Mapped[list["PostORM"]] = relationship(back_populates="user", passive_deletes=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(uuid={self.uuid}, email={self.email!r})"
