from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.post import SQLAlchemyPostRepository
from adapters.repositories.user import SQLAlchemyUserRepository
from application.interfaces.repositories.post import PostRepository
from application.interfaces.repositories.user import UserRepository


class SQLAlchemyRepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return SQLAlchemyUserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def post_repository(self, session: AsyncSession) -> PostRepository:
        return SQLAlchemyPostRepository(session=session)
