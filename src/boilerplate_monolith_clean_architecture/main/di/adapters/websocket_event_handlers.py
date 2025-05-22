from dishka import AsyncContainer, Provider, provide

from controllers.websocket.event_handlers.user import WebSocketUserEventHandler


class WebSocketEventHandlersProvider(Provider):
    @provide
    def user_event_handler(
        self,
        container: AsyncContainer,
    ) -> WebSocketUserEventHandler:
        return WebSocketUserEventHandler(
            container=container,
        )
