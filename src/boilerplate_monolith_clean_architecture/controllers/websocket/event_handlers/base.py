import logging
from collections import defaultdict
from dataclasses import dataclass, field
from json import JSONDecodeError
from typing import Any, Awaitable, Callable, get_type_hints
from uuid import UUID

from adapters.constants import WebSocketEvents
from adapters.user_uuid_provider import ContextUserUUIDProvider
from application.exceptions.base import ApplicationException
from application.interfaces.user_uuid_provider import UserUUIDProviderInterface
from controllers.dishka_inject import inject
from dishka import AsyncContainer
from domain.exceptions.base import DomainException
from fastapi.encoders import jsonable_encoder
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

user_websocket_logger = logging.getLogger("user_websocket")
webserver_logger = logging.getLogger("webserver")


@dataclass(frozen=True)
class UserWebsocketConnection:
    websocket: WebSocket
    user_uuid: UUID


@dataclass(frozen=True)
class BaseWebSocketUserEventHandler:
    container: AsyncContainer
    connections: dict[UUID, set[UserWebsocketConnection]] = field(
        default_factory=lambda: defaultdict(set), kw_only=True
    )

    async def connect(self, websocket: WebSocket, user_uuid: UUID) -> None:
        await websocket.accept()

        connection = UserWebsocketConnection(websocket, user_uuid)
        self.connections[user_uuid].add(connection)
        user_websocket_logger.debug(f"User {user_uuid} connected to websocket")
        await self._receive_events(connection)

    async def send_event(self, event: str, data: dict, user_uuid: UUID) -> None:
        data["event"] = event
        valid_json = jsonable_encoder(data)

        for connection in self.connections[user_uuid]:
            ws = connection.websocket
            await ws.send_json(valid_json)

    async def broadcast(self, event: str, data: dict) -> None:
        data["event"] = event
        valid_json = jsonable_encoder(data)
        for user in self.connections:
            for connection in self.connections[user]:
                ws = connection.websocket
                await ws.send_json(valid_json)

    async def disconnect(self, connection: UserWebsocketConnection) -> None:
        self.connections[connection.user_uuid].remove(connection)
        if len(self.connections[connection.user_uuid]) == 0:
            self.connections.pop(connection.user_uuid)

        user_websocket_logger.debug(f"User {connection.user_uuid} disconnected from websocket")

    async def _receive_events(self, connection: UserWebsocketConnection) -> None:
        try:
            while True:
                await self._receive_event(connection)
        except WebSocketDisconnect:
            await self.disconnect(connection)

    async def _receive_event(self, connection: UserWebsocketConnection) -> None:
        websocket = connection.websocket
        user_uuid = connection.user_uuid
        try:
            data: dict = await websocket.receive_json()
        except JSONDecodeError:
            await self._send_application_error("Wrong json format", user_uuid)
            return
        user_websocket_logger.debug(f"Event received from user {user_uuid}: {data=}")

        try:
            handler = self._get_event_handler(data)
        except KeyError:
            await self._send_application_error("No event is specified for processing", user_uuid)
            return
        except AttributeError:
            await self._send_application_error("The event is specified incorrectly", user_uuid)
            return
        try:
            formated_data = self._get_formated_data(handler, data)
        except ValidationError as ex:
            await self._send_application_error(str(ex.errors()), user_uuid)
            return

        try:
            async with self.container(
                context={UserUUIDProviderInterface: ContextUserUUIDProvider(user_uuid=user_uuid)}
            ) as request_container:
                await inject(handler)(formated_data, user_uuid, websocket, dishka_container=request_container)
        except WebSocketDisconnect as ex:
            raise ex
        except (DomainException, ApplicationException) as ex:
            await self._send_application_error(str(ex), user_uuid)
            return
        except Exception as ex:
            user_websocket_logger.exception(
                f"Error while processing event {handler.__name__} from user {user_uuid}: {ex}"
            )
            webserver_logger.exception(f"Error while processing event {handler.__name__} from user {user_uuid}: {ex}")
            await self._send_internal_server_error(user_uuid)
            return

    def _get_event_handler(self, data: dict) -> Callable[..., Awaitable]:
        event = data["event"]
        return getattr(self, "on_" + event)

    def _get_formated_data(self, func: Callable, data: dict) -> Any:
        type_hints = get_type_hints(func)
        data_type = type_hints.get("data")
        return data_type(**data)

    async def _send_application_error(self, detail: str, user_uuid: UUID) -> None:
        data = {"detail": detail}
        await self.send_event(WebSocketEvents.application_error.value, data, user_uuid)

    async def _send_internal_server_error(self, user_uuid: UUID) -> None:
        data = {"detail": "Internal server error"}
        await self.send_event(WebSocketEvents.internal_server_error.value, data, user_uuid)
