from dataclasses import dataclass

from application.interfaces.repositories.post import GetPostListDTO, PostListDTO, PostRepository
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.base import UseCase


@dataclass(frozen=True)
class GetPostListUseCase(UseCase[GetPostListDTO, PostListDTO]):
    repository: PostRepository
    user_uuid_provider: UserUUIDProviderInterface

    async def __call__(self, data: GetPostListDTO) -> PostListDTO:
        _user_uuid = self.user_uuid_provider.get_current_user_uuid()
        posts = await self.repository.get_list(data)
        return posts
