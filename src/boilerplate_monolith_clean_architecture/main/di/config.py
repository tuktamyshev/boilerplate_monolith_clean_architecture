from config.app import AppConfig
from config.auth import JWTAuthConfig
from config.base import Config
from config.broker import BrokerConfig
from config.db import DatabaseConfig
from config.smtp import SMTPConfig
from dishka import Provider, Scope, from_context, provide


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=Config)

    @provide
    def app_config(self, config: Config) -> AppConfig:
        return config.app

    @provide
    def auth_config(self, config: Config) -> JWTAuthConfig:
        return config.auth

    @provide
    def db_config(self, config: Config) -> DatabaseConfig:
        return config.db

    @provide
    def broker_config(self, config: Config) -> BrokerConfig:
        return config.broker

    @provide
    def smtp_config(self, config: Config) -> SMTPConfig:
        return config.smtp
