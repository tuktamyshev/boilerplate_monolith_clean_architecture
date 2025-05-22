from abc import ABC
from dataclasses import dataclass
from typing import Any

from sqlalchemy import UUID, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.orm.base import BaseORM
from application.exceptions.repository import ModelDoesNotExists
from application.interfaces.repositories.base import BaseRepository
from domain.entities.base import BaseEntity


@dataclass(frozen=True)
class SQLAlchemyRepository[ET](BaseRepository, ABC):
    session: AsyncSession
    model: BaseORM
    entity: BaseEntity

    async def create(self, entity: BaseEntity) -> ET:
        orm_model = self.model(**entity.model_dump())

        self.session.add(orm_model)
        await self.session.flush()
        await self.session.refresh(orm_model)
        return self.entity.model_validate(orm_model)

    async def delete_by_uuid(self, uuid: UUID) -> None:
        orm_model = await self.session.get(self.model, uuid)
        if not orm_model:
            raise ModelDoesNotExists()

        await self.session.delete(orm_model)
        await self.session.flush()

    async def get_one_or_none(self, **filters: Any) -> ET | None:  # noqa: ANN401
        query = select(self.model).filter_by(**filters)

        res = await self.session.execute(query)
        orm_model = res.scalar_one_or_none()
        if orm_model:
            return self.entity.model_validate(orm_model)

    async def get_one(self, **filters: Any) -> ET:  # noqa: ANN401
        query = select(self.model).filter_by(**filters)

        res = await self.session.execute(query)
        try:
            orm_model = res.scalar_one()
        except NoResultFound:
            raise ModelDoesNotExists()

        return self.entity.model_validate(orm_model)

    async def update(self, uuid: UUID, **kwargs: Any) -> ET:  # noqa: ANN401
        orm_model = await self.session.get_one(self.model, uuid)
        for name, value in kwargs.items():
            setattr(orm_model, name, value)
        await self.session.flush()
        await self.session.refresh(orm_model)
        return self.entity.model_validate(orm_model)
