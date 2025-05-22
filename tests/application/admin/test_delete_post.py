from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from application.use_cases.admin.delete_post import AdminDeletePostUseCase
from domain.exceptions.access import AccessException
from domain.exceptions.post import PostDoesNotExistsException


class TestAdminDeletePostUseCase:
    def setup_method(self):
        self.post_repository = AsyncMock()
        self.transaction_manager = AsyncMock()
        self.check_is_admin_use_case = AsyncMock()
        self.use_case = AdminDeletePostUseCase(
            post_repository=self.post_repository,
            transaction_manager=self.transaction_manager,
            check_is_admin_use_case=self.check_is_admin_use_case,
        )

    async def test_delete_post_success(self):
        post_uuid = uuid4()
        await self.use_case(post_uuid)

        self.check_is_admin_use_case.assert_awaited_once()
        self.post_repository.delete_by_uuid.assert_awaited_once_with(post_uuid)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()

    async def test_delete_post_not_admin(self):
        post_uuid = uuid4()
        self.check_is_admin_use_case.side_effect = AccessException()

        with pytest.raises(AccessException):
            await self.use_case(post_uuid)

        self.check_is_admin_use_case.assert_awaited_once()
        self.post_repository.delete_by_uuid.assert_not_awaited()
        self.transaction_manager.__aenter__.assert_not_called()
        self.transaction_manager.__aexit__.assert_not_called()

    async def test_delete_post_not_exists(self):
        post_uuid = uuid4()
        self.post_repository.delete_by_uuid.side_effect = PostDoesNotExistsException(post_uuid)

        with pytest.raises(PostDoesNotExistsException):
            await self.use_case(post_uuid)

        self.check_is_admin_use_case.assert_awaited_once()
        self.post_repository.delete_by_uuid.assert_awaited_once_with(post_uuid)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()
