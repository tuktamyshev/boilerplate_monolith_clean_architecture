from dataclasses import dataclass

from pydantic import BaseModel

from application.interfaces.analyze_service import AnalyzePostServiceInterface
from application.interfaces.repositories.post import PostRepository
from application.interfaces.transaction_manager import TransactionManager
from application.interfaces.user_notificator import NotifyNewPostDTO, UserNotificatorInterface
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.base import UseCase
from domain.entities.post import PostEntity
from domain.value_objects.post_text import PostTextValueObject


class CreatePostDTO(BaseModel):
    text: PostTextValueObject


@dataclass(frozen=True)
class CreatePostUseCase(UseCase[CreatePostDTO, PostEntity]):
    transaction_manager: TransactionManager
    post_repository: PostRepository
    user_uuid_provider: UserUUIDProviderInterface
    user_notificator: UserNotificatorInterface
    post_analyze_post_service: AnalyzePostServiceInterface

    async def __call__(self, data: CreatePostDTO) -> PostEntity:
        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        post_entity = PostEntity.create(
            text=data.text,
            user_uuid=user_uuid,
        )
        async with self.transaction_manager:
            await self.post_repository.create(post_entity)

        await self.user_notificator.notify_new_post(
            data=NotifyNewPostDTO(
                **post_entity.model_dump(),
            )
        )
        await self.post_analyze_post_service.analyze_post(post_entity)
        return post_entity
