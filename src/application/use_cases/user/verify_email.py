from dataclasses import dataclass

from application.interfaces.email import EmailServiceInterface
from application.interfaces.repositories.user import UserRepository
from application.interfaces.transaction_manager import TransactionManager
from application.use_cases.base import UseCase
from domain.entities.user import UserEntity


@dataclass(frozen=True)
class VerifyEmailUseCase(UseCase):
    user_repository: UserRepository
    email_service: EmailServiceInterface
    transaction_manager: TransactionManager

    async def __call__(self, data: str) -> UserEntity:
        token = data
        email = self.email_service.verify_email(token)

        user = await self.user_repository.get_one(email=email)

        async with self.transaction_manager:
            user = await self.user_repository.update(user.uuid, is_verified=True)

        return user
