from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from application.dtos.pagination import PaginatedRequestDTO, PaginatedResponseDTO
from application.interfaces.repositories.base import BaseRepository
from domain.entities.post import PostEntity
from domain.value_objects.post_text import PostTextValueObject
from pydantic import BaseModel, ConfigDict


class PostInfoDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    user_uuid: UUID
    text: PostTextValueObject
    created_at: datetime


class PostListDTO(PaginatedResponseDTO[PostInfoDTO]):
    pass


class GetPostListDTO(PaginatedRequestDTO):
    text: PostTextValueObject | None
    date_from: datetime | None
    date_to: datetime | None
    user_uuid: UUID | None


@dataclass(frozen=True)
class PostRepository(BaseRepository[PostEntity], ABC):
    def get_list(self, filters: GetPostListDTO) -> PostListDTO: ...
