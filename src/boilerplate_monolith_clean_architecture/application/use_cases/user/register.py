from dataclasses import dataclass

from application.dtos.user import UserEmailDTO
from application.exceptions.user import UserWithThisEmailAlreadyExistsException
from application.interfaces.email import EmailServiceInterface
from application.interfaces.password_hasher import PasswordHasherInterface
from application.interfaces.repositories.user import UserRepository
from application.interfaces.transaction_manager import TransactionManager
from application.use_cases.base import UseCase
from domain.entities.user import UserEntity


class UserCreateDTO(UserEmailDTO):
    password: str


@dataclass(frozen=True)
class RegisterUserUseCase(UseCase[UserCreateDTO, UserEntity]):
    user_repository: UserRepository
    transaction_manager: TransactionManager
    email_service: EmailServiceInterface
    password_hasher_service: PasswordHasherInterface

    async def __call__(self, data: UserCreateDTO) -> UserEntity:
        hashed_password = self.password_hasher_service.hash_password(data.password)

        existing = await self.user_repository.get_one_or_none(email=data.email)
        if existing and existing.is_verified:
            raise UserWithThisEmailAlreadyExistsException(email=data.email)

        user_entity = UserEntity.create(email=data.email, hashed_password=hashed_password)

        async with self.transaction_manager:
            if existing:
                await self.user_repository.update(existing.uuid, **user_entity.model_dump(exclude={"uuid"}))
            else:
                await self.user_repository.create(user_entity)

        await self.email_service.send_verification_to_email(data.email)

        return user_entity
