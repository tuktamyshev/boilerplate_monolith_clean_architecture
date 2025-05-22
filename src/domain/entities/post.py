from datetime import datetime
from uuid import UUID, uuid4

from domain.entities.base import BaseEntity
from domain.value_objects.post_text import PostTextValueObject


class PostEntity(BaseEntity):
    user_uuid: UUID
    text: PostTextValueObject

    @classmethod
    def create(cls, user_uuid: UUID, text: PostTextValueObject) -> "PostEntity":
        return PostEntity(
            uuid=uuid4(),
            created_at=datetime.now(),
            user_uuid=user_uuid,
            text=text,
        )
