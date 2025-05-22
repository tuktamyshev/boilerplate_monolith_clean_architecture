from dataclasses import dataclass

from adapters.orm.user import UserORM
from adapters.repositories.base import SQLAlchemyRepository
from application.exceptions.user import UserWithThisEmailAlreadyExistsException, UserWithThisEmailDoesNotExistsException
from application.interfaces.repositories.user import UserRepository
from asyncpg.exceptions import UniqueViolationError
from domain.entities.user import UserEntity
from domain.value_objects.email import EmailValueObject
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


@dataclass(frozen=True)
class SQLAlchemyUserRepository(UserRepository, SQLAlchemyRepository):
    model: UserORM = UserORM
    entity: UserEntity = UserEntity

    async def create(self, entity: UserEntity) -> UserEntity:
        try:
            return await super().create(entity)
        except IntegrityError as e:
            error_message = str(e.orig)
            if UniqueViolationError.__name__ in error_message:  # noqa: SIM102
                if "email" in error_message:
                    raise UserWithThisEmailAlreadyExistsException(email=entity.email)
            raise e

    async def delete_by_email(self, email: EmailValueObject) -> None:
        stmt = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserWithThisEmailDoesNotExistsException(email=email)

        await self.session.delete(user)
