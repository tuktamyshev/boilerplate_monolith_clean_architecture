from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel

from application.interfaces.user_notificator import SendMessageToAnotherUserDTO, UserNotificatorInterface
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from application.use_cases.base import UseCase


class MessageToAnotherUserDTO(BaseModel):
    user_uuid: UUID
    message: str


@dataclass(frozen=True)
class MessageFromUserUseCase(UseCase[MessageToAnotherUserDTO, None]):
    user_notificator: UserNotificatorInterface
    user_uuid_provider: UserUUIDProviderInterface

    async def __call__(self, data: MessageToAnotherUserDTO) -> None:
        user_uuid = self.user_uuid_provider.get_current_user_uuid()
        await self.user_notificator.send_message_to_user_from_another_user(
            SendMessageToAnotherUserDTO(
                user_uuid_from=user_uuid,
                text=data.message,
            ),
            user_uuid=data.user_uuid,
        )
