from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, WebSocketException
from fastapi.websockets import WebSocket
from starlette import status

from application.exceptions.auth import AuthenticationException
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from controllers.websocket.event_handlers.user import WebSocketUserEventHandler

router = APIRouter(
    prefix="/ws",
)


@router.websocket("/web_client")
@inject
async def web_client_websocket_endpoint(
    websocket: WebSocket,
    event_handler: FromDishka[WebSocketUserEventHandler],
    user_uuid_provider: FromDishka[UserUUIDProviderInterface],
) -> None:
    try:
        user_uuid = user_uuid_provider.get_current_user_uuid()
    except AuthenticationException:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    await event_handler.connect(websocket, user_uuid)
