from adapters.user_notificator import WebSocketUserNotificator
from application.interfaces.user_notificator import UserNotificatorInterface
from dishka import Provider, provide


class WebSocketUserNotificatorProvider(Provider):
    user_notificator = provide(WebSocketUserNotificator, provides=UserNotificatorInterface)
