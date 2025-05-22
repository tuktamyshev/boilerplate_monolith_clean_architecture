from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from config.base import Config


class SQLAlchemyDatabaseProvider(Provider):
    @provide
    def db_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(
            config.db.URI,
            echo=config.db.ECHO,
            echo_pool=config.db.ECHO_POOL,
            pool_size=config.db.POOL_SIZE,
            max_overflow=config.db.MAX_OVERFLOW,
        )

    @provide
    def db_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def db_session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session
