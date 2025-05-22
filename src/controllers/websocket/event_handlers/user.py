from dataclasses import dataclass
from uuid import UUID

from dishka import FromDishka
from starlette.websockets import WebSocket

from application.use_cases.message_from_user import MessageFromUserUseCase, MessageToAnotherUserDTO
from controllers.websocket.event_handlers.base import BaseWebSocketUserEventHandler


@dataclass(frozen=True)
class WebSocketUserEventHandler(BaseWebSocketUserEventHandler):
    # It only works for one server instance, otherwise you need to send an event to all instances,
    # for example via redis pub\sub as in socketio
    async def on_ping(
        self,
        data: dict,
        user_uuid: UUID,
        ws: WebSocket,
    ) -> None:
        await self.send_event("pong", {}, user_uuid)

    async def on_send_message(
        self,
        data: MessageToAnotherUserDTO,
        user_uuid: UUID,
        ws: WebSocket,
        use_case: FromDishka[MessageFromUserUseCase],
    ) -> None:
        # Example receiving events from user
        await use_case(data)

    # async def on_ ...
