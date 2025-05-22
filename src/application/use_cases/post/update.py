from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel

from application.interfaces.repositories.post import PostRepository
from application.interfaces.transaction_manager import TransactionManager
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.base import UseCase
from domain.entities.post import PostEntity
from domain.services.access import AccessService


class UpdatePostDTO(BaseModel):
    uuid: UUID
    text: str | None


@dataclass(frozen=True)
class UpdatePostUseCase(UseCase[UpdatePostDTO, PostEntity]):
    transaction_manager: TransactionManager
    post_repository: PostRepository
    user_uuid_provider: UserUUIDProviderInterface
    access_service: AccessService

    async def __call__(self, data: UpdatePostDTO) -> PostEntity:
        post_entity = await self.post_repository.get_one(uuid=data.uuid)
        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        self.access_service.check_is_owner(user_uuid, post_entity)

        async with self.transaction_manager:
            await self.post_repository.update(post_entity.uuid, **data.model_dump(exclude={"uuid"}))

        return post_entity
