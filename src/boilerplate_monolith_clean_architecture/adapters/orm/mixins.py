from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from .user import UserORM


class UserRelationMixin:
    _user_uuid_nullable: bool = False
    _user_uuid_unique: bool = False
    _user_back_populates: str | None = None
    _user_on_delete: str = "CASCADE"

    @declared_attr
    def user_uuid(cls) -> Mapped[UUID]:
        return mapped_column(
            ForeignKey("user.uuid", ondelete=cls._user_on_delete),
            unique=cls._user_uuid_unique,
            nullable=cls._user_uuid_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped["UserORM"]:
        return relationship(
            "UserORM",
            back_populates=cls._user_back_populates,
        )
