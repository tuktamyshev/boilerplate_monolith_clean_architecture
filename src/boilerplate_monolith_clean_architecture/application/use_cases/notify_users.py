from dataclasses import dataclass

from application.interfaces.user_notificator import NotifyUsersDTO, UserNotificatorInterface
from application.use_cases.base import UseCase


@dataclass(frozen=True)
class NotifyUsersUseCase(UseCase[NotifyUsersDTO, None]):
    user_notificator: UserNotificatorInterface

    async def __call__(self, data: NotifyUsersDTO) -> None:
        await self.user_notificator.notify_users_about_something(NotifyUsersDTO(**data.model_dump()))
