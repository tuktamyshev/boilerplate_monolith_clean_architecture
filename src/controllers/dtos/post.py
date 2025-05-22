from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from controllers.dtos.pagination import InfraPaginationDTO
from domain.value_objects.post_text import PostTextValueObject


class ReadPostDTO(BaseModel):
    uuid: UUID
    created_at: datetime
    user_uuid: UUID
    text: PostTextValueObject


class PostFilter(InfraPaginationDTO):
    user_uuid: UUID | None = Field(None)
    text: PostTextValueObject | None = Field(None, max_length=1024)
    date_from: datetime | None = Field(None)
    date_to: datetime | None = Field(None)
