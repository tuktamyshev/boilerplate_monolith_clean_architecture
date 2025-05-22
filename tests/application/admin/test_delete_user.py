from unittest.mock import AsyncMock

import pytest

from application.use_cases.admin.delete_user import AdminDeleteUserUseCase
from domain.exceptions.access import AccessException
from domain.value_objects.email import EmailValueObject


class TestAdminDeleteUserUseCase:
    def setup_method(self):
        self.user_repository = AsyncMock()
        self.transaction_manager = AsyncMock()
        self.check_is_admin_use_case = AsyncMock()
        self.use_case = AdminDeleteUserUseCase(
            user_repository=self.user_repository,
            transaction_manager=self.transaction_manager,
            check_is_admin_use_case=self.check_is_admin_use_case,
        )

    async def test_delete_user_success(self):
        email = EmailValueObject("test@example.com")
        await self.use_case(email)

        self.check_is_admin_use_case.assert_awaited_once()
        self.user_repository.delete_by_email.assert_awaited_once_with(email)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()

    async def test_delete_user_not_admin(self):
        email = EmailValueObject("test@example.com")
        self.check_is_admin_use_case.side_effect = AccessException()

        with pytest.raises(AccessException):
            await self.use_case(email)

        self.check_is_admin_use_case.assert_awaited_once()
        self.user_repository.delete_by_email.assert_not_awaited()
        self.transaction_manager.__aenter__.assert_not_called()
        self.transaction_manager.__aexit__.assert_not_called()
