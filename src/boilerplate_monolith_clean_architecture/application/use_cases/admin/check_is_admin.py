from dataclasses import dataclass
from uuid import UUID

from application.interfaces.repositories.user import UserRepository
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.base import UseCase
from domain.services.access import AccessService


@dataclass(frozen=True)
class CheckIsAdminUseCase(UseCase[UUID, None]):
    user_uuid_provider: UserUUIDProviderInterface
    access_service: AccessService
    user_repository: UserRepository

    async def __call__(self, data: None = None) -> None:
        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        user = await self.user_repository.get_one(uuid=user_uuid)
        self.access_service.check_is_admin(user)
