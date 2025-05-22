from unittest.mock import AsyncMock, MagicMock

from application.interfaces.repositories.post import GetPostListDTO, PostInfoDTO, PostListDTO
from application.use_cases.post.get_list import GetPostListUseCase

from tests.factories.entities import PostEntityFactory, UserEntityFactory


class TestGetPostListUseCase:
    def setup_method(self) -> None:
        self.post_repository = AsyncMock()
        self.user_uuid_provider = MagicMock()
        self.user = UserEntityFactory()
        self.user_uuid_provider.get_current_user_uuid.return_value = self.user.uuid
        self.use_case = GetPostListUseCase(
            repository=self.post_repository,
            user_uuid_provider=self.user_uuid_provider,
        )

    async def test_get_post_list_success(self) -> None:
        dto = GetPostListDTO(limit=2, offset=0, text=None, date_from=None, date_to=None, user_uuid=None)
        posts = [PostEntityFactory(), PostEntityFactory()]
        expected_result = PostListDTO(items=posts, total=2)
        self.post_repository.get_list.return_value = expected_result

        result = await self.use_case(dto)

        assert result == expected_result
        assert len(result.items) == 2
        assert all(isinstance(post, PostInfoDTO) for post in result.items)
        assert result.total == 2
        self.post_repository.get_list.assert_awaited_once_with(dto)
