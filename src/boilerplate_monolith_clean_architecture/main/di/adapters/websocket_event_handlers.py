from controllers.websocket.event_handlers.user import WebSocketUserEventHandler
from dishka import AsyncContainer, Provider, provide


class WebSocketEventHandlersProvider(Provider):
    @provide
    def user_event_handler(
        self,
        container: AsyncContainer,
    ) -> WebSocketUserEventHandler:
        return WebSocketUserEventHandler(
            container=container,
        )
