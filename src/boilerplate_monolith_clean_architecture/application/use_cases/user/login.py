from dataclasses import dataclass
from uuid import UUID

from application.dtos.user import UserEmailDTO
from application.exceptions.auth import InactiveUserException, WrongEmailOrPasswordException
from application.interfaces.password_hasher import PasswordHasherInterface
from application.interfaces.repositories.user import UserRepository
from application.use_cases.base import UseCase
from domain.value_objects.email import EmailValueObject


class UserLoginDTO(UserEmailDTO):
    password: str


@dataclass(frozen=True)
class LoginUserUseCase(UseCase[UserLoginDTO, UUID]):
    user_repository: UserRepository
    password_hasher_service: PasswordHasherInterface

    async def __call__(self, data: UserLoginDTO) -> UUID:
        return await self._validate_user_login(data.email, data.password)

    async def _validate_user_login(self, email: EmailValueObject, password: str) -> UUID:
        if not (user := await self.user_repository.get_one_or_none(email=email)):
            raise WrongEmailOrPasswordException()

        if not self.password_hasher_service.validate_password(
            password=password,
            hashed_password=user.hashed_password,
        ):
            raise WrongEmailOrPasswordException()

        if not user.is_verified:
            raise WrongEmailOrPasswordException()

        if not user.is_active:
            raise InactiveUserException()

        return user.uuid
