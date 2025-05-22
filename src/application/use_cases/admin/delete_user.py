from dataclasses import dataclass

from application.interfaces.repositories.user import UserRepository
from application.interfaces.transaction_manager import TransactionManager
from application.use_cases.admin.check_is_admin import CheckIsAdminUseCase
from application.use_cases.base import UseCase


@dataclass(frozen=True)
class AdminDeleteUserUseCase(UseCase[str, None]):
    user_repository: UserRepository
    transaction_manager: TransactionManager
    check_is_admin_use_case: CheckIsAdminUseCase

    async def __call__(self, data: str) -> None:
        await self.check_is_admin_use_case()

        user_email = data
        async with self.transaction_manager:
            await self.user_repository.delete_by_email(user_email)
