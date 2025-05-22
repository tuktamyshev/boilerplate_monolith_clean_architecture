from dishka import Scope

from main.di.adapters.analyze_service import AnalyzeServiceProvider
from main.di.adapters.auth import JWTAuthServiceProvider
from main.di.adapters.broker import KafkaBrokerProvider
from main.di.adapters.cookie_service import CookieServiceProvider
from main.di.adapters.database import SQLAlchemyDatabaseProvider
from main.di.adapters.email_service import DevelopEmailServiceProvider, EmailServiceProvider
from main.di.adapters.password_hasher import PasswordHasherProvider
from main.di.adapters.repositories import SQLAlchemyRepositoriesProvider
from main.di.adapters.transaction_manager import SQLAlchemyTransactionManagerProvider
from main.di.adapters.user_notificator import WebSocketUserNotificatorProvider
from main.di.adapters.user_uuid_provider import TokenUserUUIDProviderProvider
from main.di.adapters.websocket_event_handlers import WebSocketEventHandlersProvider


class AdaptersProvider(
    # Adapters that are not tied to business logic and do not implement interfaces
    WebSocketEventHandlersProvider,
    CookieServiceProvider,
    JWTAuthServiceProvider,
    KafkaBrokerProvider,
    SQLAlchemyDatabaseProvider,
    # Realizations of interfaces
    SQLAlchemyTransactionManagerProvider,
    AnalyzeServiceProvider,
    TokenUserUUIDProviderProvider,
    SQLAlchemyRepositoriesProvider,
    WebSocketUserNotificatorProvider,
    EmailServiceProvider,
    PasswordHasherProvider,
):
    scope = Scope.APP


class DevelopmentAdaptersProvider(
    # Overwritten adapters for development
    DevelopEmailServiceProvider,
    AdaptersProvider,
):
    scope = Scope.APP
