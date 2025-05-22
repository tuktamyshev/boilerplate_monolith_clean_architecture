from dataclasses import dataclass
from uuid import UUID

from application.exceptions.repository import ModelDoesNotExists
from application.interfaces.repositories.post import PostRepository
from application.interfaces.transaction_manager import TransactionManager
from application.use_cases.admin.check_is_admin import CheckIsAdminUseCase
from application.use_cases.base import UseCase
from domain.exceptions.post import PostDoesNotExistsException


@dataclass(frozen=True)
class AdminDeletePostUseCase(UseCase[UUID, None]):
    post_repository: PostRepository
    transaction_manager: TransactionManager
    check_is_admin_use_case: CheckIsAdminUseCase

    async def __call__(self, data: UUID) -> None:
        await self.check_is_admin_use_case()

        post_uuid = data
        async with self.transaction_manager:
            try:
                await self.post_repository.delete_by_uuid(post_uuid)
            except ModelDoesNotExists:
                raise PostDoesNotExistsException(post_uuid)
