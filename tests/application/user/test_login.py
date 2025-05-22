from unittest.mock import AsyncMock, MagicMock

import pytest
from application.exceptions.auth import InactiveUserException, WrongEmailOrPasswordException
from application.use_cases.user.login import LoginUserUseCase, UserLoginDTO
from domain.value_objects.email import EmailValueObject

from tests.factories.entities import UserEntityFactory


class TestLoginUserUseCase:
    def setup_method(self) -> None:
        self.user_repository = AsyncMock()
        self.password_hasher_service = MagicMock()
        self.use_case = LoginUserUseCase(
            user_repository=self.user_repository,
            password_hasher_service=self.password_hasher_service,
        )

    async def test_login_success(self) -> None:
        user = UserEntityFactory(is_verified=True, is_active=True)
        password = "password123"
        self.user_repository.get_one_or_none.return_value = user
        self.password_hasher_service.validate_password.return_value = True

        dto = UserLoginDTO(email=user.email, password=password)
        result = await self.use_case(dto)

        assert result == user.uuid
        self.user_repository.get_one_or_none.assert_awaited_once_with(email=user.email)
        self.password_hasher_service.validate_password.assert_called_once_with(
            password=password,
            hashed_password=user.hashed_password,
        )

    async def test_login_wrong_credentials(self) -> None:
        email = EmailValueObject("test@example.com")
        password = "wrong_password"
        self.user_repository.get_one_or_none.return_value = None

        dto = UserLoginDTO(email=email, password=password)

        with pytest.raises(WrongEmailOrPasswordException):
            await self.use_case(dto)

    async def test_login_inactive_user(self) -> None:
        user = UserEntityFactory(is_verified=True, is_active=False)
        password = "password123"
        self.user_repository.get_one_or_none.return_value = user
        self.password_hasher_service.validate_password.return_value = True

        dto = UserLoginDTO(email=user.email, password=password)

        with pytest.raises(InactiveUserException):
            await self.use_case(dto)

    async def test_login_unverified_user(self) -> None:
        user = UserEntityFactory(is_verified=False, is_active=True)
        password = "password123"
        self.user_repository.get_one_or_none.return_value = user
        self.password_hasher_service.validate_password.return_value = True

        dto = UserLoginDTO(email=user.email, password=password)

        with pytest.raises(WrongEmailOrPasswordException):
            await self.use_case(dto)
