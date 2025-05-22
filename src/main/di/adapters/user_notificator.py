from dishka import Provider, provide

from adapters.user_notificator import WebSocketUserNotificator
from application.interfaces.user_notificator import UserNotificatorInterface


class WebSocketUserNotificatorProvider(Provider):
    user_notificator = provide(WebSocketUserNotificator, provides=UserNotificatorInterface)
