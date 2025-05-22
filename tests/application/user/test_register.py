import pytest
from unittest.mock import AsyncMock, MagicMock

from application.use_cases.user.register import RegisterUserUseCase, UserCreateDTO
from application.exceptions.user import UserWithThisEmailAlreadyExistsException
from domain.entities.user import UserEntity
from domain.value_objects.email import EmailValueObject
from tests.factories.entities import UserEntityFactory


class TestRegisterUserUseCase:
    def setup_method(self):
        self.user_repository = AsyncMock()
        self.transaction_manager = AsyncMock()
        self.email_service = AsyncMock()
        self.password_hasher_service = MagicMock()
        self.use_case = RegisterUserUseCase(
            user_repository=self.user_repository,
            transaction_manager=self.transaction_manager,
            email_service=self.email_service,
            password_hasher_service=self.password_hasher_service,
        )

    async def test_register_user_success(self):
        email = EmailValueObject("test@example.com")
        password = "password123"
        hashed_password = "hashed_password"
        self.password_hasher_service.hash_password.return_value = hashed_password
        self.user_repository.get_one_or_none.return_value = None

        dto = UserCreateDTO(email=email, password=password)
        result = await self.use_case(dto)

        assert isinstance(result, UserEntity)
        assert result.email == EmailValueObject(email)
        assert result.hashed_password == hashed_password
        assert not result.is_verified
        self.password_hasher_service.hash_password.assert_called_once_with(password)
        self.user_repository.create.assert_awaited_once()
        self.email_service.send_verification_to_email.assert_awaited_once_with(email)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()

    async def test_register_user_already_exists(self):
        email = EmailValueObject("test@example.com")
        password = "password123"
        existing_user = UserEntityFactory(is_verified=True)
        self.user_repository.get_one_or_none.return_value = existing_user

        dto = UserCreateDTO(email=email, password=password)

        with pytest.raises(UserWithThisEmailAlreadyExistsException):
            await self.use_case(dto)

        self.user_repository.create.assert_not_awaited()
        self.email_service.send_verification_to_email.assert_not_awaited()
        self.transaction_manager.__aenter__.assert_not_called()
        self.transaction_manager.__aexit__.assert_not_called()
