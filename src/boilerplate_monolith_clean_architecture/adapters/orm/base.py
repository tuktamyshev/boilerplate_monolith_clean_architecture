import re
from datetime import datetime

from sqlalchemy import UUID, DateTime, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class BaseORM(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

    @declared_attr
    def __tablename__(cls) -> str:
        table_name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__.rstrip("ORM"))
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", table_name).lower()

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return str(self)
