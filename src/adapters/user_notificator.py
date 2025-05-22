from dataclasses import dataclass
from uuid import UUID

from adapters.constants import WebSocketEvents
from application.interfaces.user_notificator import (
    NotifyNewPostDTO,
    NotifyUsersDTO,
    SendMessageToAnotherUserDTO,
    UserNotificatorInterface,
)
from controllers.websocket.event_handlers.user import WebSocketUserEventHandler


@dataclass(frozen=True)
class WebSocketUserNotificator(UserNotificatorInterface):
    web_socket_event_handler: WebSocketUserEventHandler

    async def send_message_to_user_from_another_user(self, data: SendMessageToAnotherUserDTO, user_uuid: UUID) -> None:
        await self.web_socket_event_handler.send_event(
            WebSocketEvents.message.value,
            data=data.model_dump(),
            user_uuid=user_uuid,
        )

    async def notify_new_post(self, data: NotifyNewPostDTO) -> None:
        await self.web_socket_event_handler.broadcast(
            WebSocketEvents.new_post.value,
            data=data.model_dump(),
        )

    async def notify_users_about_something(self, data: NotifyUsersDTO) -> None:
        await self.web_socket_event_handler.broadcast(
            WebSocketEvents.notify_about_something.value,
            data=data.model_dump(),
        )
