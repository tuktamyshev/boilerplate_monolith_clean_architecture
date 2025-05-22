from dataclasses import dataclass
from uuid import UUID

from application.exceptions.repository import ModelDoesNotExists
from application.interfaces.repositories.post import PostRepository
from application.interfaces.transaction_manager import TransactionManager
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.base import UseCase
from domain.exceptions.post import PostDoesNotExistsException
from domain.services.access import AccessService


@dataclass(frozen=True)
class DeletePostUseCase(UseCase[UUID, None]):
    transaction_manager: TransactionManager
    post_repository: PostRepository
    user_uuid_provider: UserUUIDProviderInterface
    access_service: AccessService

    async def __call__(self, data: UUID) -> None:
        post_uuid = data

        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        try:
            post_entity = await self.post_repository.get_one(uuid=post_uuid)
        except ModelDoesNotExists:
            raise PostDoesNotExistsException(post_uuid)

        self.access_service.check_is_owner(user_uuid, post_entity)

        async with self.transaction_manager:
            await self.post_repository.delete_by_uuid(post_uuid)
