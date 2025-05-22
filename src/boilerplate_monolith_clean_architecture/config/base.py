from config import BASE_DIR
from config.app import AppConfig
from config.auth import JWTAuthConfig
from config.broker import BrokerConfig
from config.db import DatabaseConfig
from config.smtp import SMTPConfig
from config.worker import WorkerConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(f"{BASE_DIR}/env/.env.default", f"{BASE_DIR}/env/.env"),
        env_nested_delimiter="__",
    )

    app: AppConfig
    auth: JWTAuthConfig
    db: DatabaseConfig
    broker: BrokerConfig
    worker: WorkerConfig
    smtp: SMTPConfig
