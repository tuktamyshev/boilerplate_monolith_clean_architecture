import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from src.boilerplate_monolith_clean_architecture.main.database.alembic import BaseORM

# alembic takes variables only from .env
load_dotenv(find_dotenv("env/.env"))

config = context.config
config.set_main_option(
    "sqlalchemy.url",
    "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
        user=os.getenv("DB__USER"),
        password=os.getenv("DB__PASSWORD"),
        host=os.getenv("DB__HOST"),
        port=os.getenv("DB__PORT"),
        db=os.getenv("DB__NAME"),
    ),
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseORM.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
