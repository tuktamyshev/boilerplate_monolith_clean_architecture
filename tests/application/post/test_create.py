from unittest.mock import AsyncMock, MagicMock, patch

from application.interfaces.user_notificator import NotifyNewPostDTO
from application.use_cases.post.create import CreatePostDTO, CreatePostUseCase
from domain.entities.post import PostEntity
from tests.factories.entities import PostEntityFactory, UserEntityFactory


class TestCreatePostUseCase:
    def setup_method(self) -> None:
        self.post_repository = AsyncMock()
        self.user_uuid_provider = MagicMock()
        self.user_notificator = AsyncMock()
        self.analyze_service = AsyncMock()
        self.transaction_manager = AsyncMock()
        self.user = UserEntityFactory()
        self.user_uuid_provider.get_current_user_uuid.return_value = self.user.uuid
        self.use_case = CreatePostUseCase(
            transaction_manager=self.transaction_manager,
            post_repository=self.post_repository,
            user_uuid_provider=self.user_uuid_provider,
            user_notificator=self.user_notificator,
            post_analyze_post_service=self.analyze_service,
        )

    async def test_create_post_success(self) -> None:
        post_entity = PostEntityFactory(user_uuid=self.user.uuid)
        dto = CreatePostDTO(text=post_entity.text)
        with patch("application.use_cases.post.create.PostEntity.create", return_value=post_entity) as mock_create:
            result = await self.use_case(dto)

            mock_create.assert_called_once_with(text=post_entity.text, user_uuid=self.user.uuid)

        assert isinstance(result, PostEntity)
        assert result.text == post_entity.text
        assert result.user_uuid == self.user.uuid
        self.post_repository.create.assert_awaited_once_with(post_entity)
        self.user_notificator.notify_new_post.assert_awaited_once_with(
            data=NotifyNewPostDTO(**post_entity.model_dump())
        )
        self.analyze_service.analyze_post.assert_awaited_once_with(post_entity)
        self.transaction_manager.__aenter__.assert_called_once()
        self.transaction_manager.__aexit__.assert_called_once()
