from unittest.mock import AsyncMock, MagicMock

from application.use_cases.user.verify_email import VerifyEmailUseCase
from domain.entities.user import UserEntity
from tests.factories.entities import UserEntityFactory


class TestVerifyEmailUseCase:
    def setup_method(self) -> None:
        self.user_repository = AsyncMock()
        self.email_service = MagicMock()
        self.transaction_manager = AsyncMock()
        self.use_case = VerifyEmailUseCase(
            user_repository=self.user_repository,
            email_service=self.email_service,
            transaction_manager=self.transaction_manager,
        )

    async def test_verify_email_success(self) -> None:
        user = UserEntityFactory(is_verified=False)
        updated_user = UserEntityFactory(is_verified=True, uuid=user.uuid, email=user.email)
        token = "verification_token"
        self.email_service.verify_email.return_value = user.email
        self.user_repository.get_one.return_value = user
        self.user_repository.update.return_value = updated_user

        result = await self.use_case(token)

        assert isinstance(result, UserEntity)
        assert result.is_verified
        self.email_service.verify_email.assert_called_once_with(token)
        self.user_repository.get_one.assert_awaited_once_with(email=user.email)
        self.user_repository.update.assert_awaited_once_with(user.uuid, is_verified=True)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()
