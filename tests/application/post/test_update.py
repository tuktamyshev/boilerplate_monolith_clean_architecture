import pytest
from unittest.mock import AsyncMock, MagicMock

from application.use_cases.post.update import UpdatePostDTO, UpdatePostUseCase
from domain.entities.post import PostEntity
from domain.exceptions.access import AccessException
from domain.value_objects.post_text import PostTextValueObject
from tests.factories.entities import PostEntityFactory, UserEntityFactory

class TestUpdatePostUseCase:
    def setup_method(self):
        self.post_repository = AsyncMock()
        self.user_uuid_provider = MagicMock()
        self.access_service = MagicMock()
        self.transaction_manager = AsyncMock()
        self.user = UserEntityFactory()
        self.post = PostEntityFactory(user_uuid=self.user.uuid)
        self.user_uuid_provider.get_current_user_uuid.return_value = self.user.uuid
        self.post_repository.get_one.return_value = self.post
        self.use_case = UpdatePostUseCase(
            transaction_manager=self.transaction_manager,
            post_repository=self.post_repository,
            user_uuid_provider=self.user_uuid_provider,
            access_service=self.access_service,
        )

    async def test_update_post_success(self):
        new_text = PostTextValueObject("Updated text")
        dto = UpdatePostDTO(uuid=self.post.uuid, text=new_text)

        result = await self.use_case(dto)

        assert isinstance(result, PostEntity)
        self.post_repository.get_one.assert_awaited_once_with(uuid=self.post.uuid)
        self.access_service.check_is_owner.assert_called_once_with(self.user.uuid, self.post)
        self.post_repository.update.assert_awaited_once_with(
            self.post.uuid,
            text=new_text
        )
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()

    async def test_update_post_not_owner(self):
        other_user = UserEntityFactory()
        self.user_uuid_provider.get_current_user_uuid.return_value = other_user.uuid
        self.access_service.check_is_owner.side_effect = AccessException()
        new_text = PostTextValueObject("Updated text")
        dto = UpdatePostDTO(uuid=self.post.uuid, text=new_text)

        with pytest.raises(AccessException):
            await self.use_case(dto)

        self.post_repository.get_one.assert_awaited_once_with(uuid=self.post.uuid)
        self.access_service.check_is_owner.assert_called_once_with(other_user.uuid, self.post)
        self.post_repository.update.assert_not_awaited()
        self.transaction_manager.__aenter__.assert_not_called()
        self.transaction_manager.__aexit__.assert_not_called()
