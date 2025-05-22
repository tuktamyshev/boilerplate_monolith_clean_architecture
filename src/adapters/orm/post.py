from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from adapters.orm.base import BaseORM
from adapters.orm.mixins import UserRelationMixin
from domain.value_objects.post_text import PostTextValueObject


class PostORM(BaseORM, UserRelationMixin):
    _user_back_populates = "posts"

    text: Mapped[PostTextValueObject] = mapped_column(String())

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.uuid}, created_at={self.created_at}, user_uuid={self.user_uuid})"
