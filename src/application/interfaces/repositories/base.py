from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID


@dataclass(frozen=True)
class BaseRepository[ET](
    ABC
):  # TODO split into interfaces and inherit only the necessary interfaces in implementations
    @abstractmethod
    async def create(self, entity: ET) -> ET: ...

    @abstractmethod
    async def delete_by_uuid(self, uuid: UUID) -> None: ...

    @abstractmethod
    async def get_one_or_none(self, **kwargs: Any) -> Optional[ET]: ...  # noqa: ANN401

    @abstractmethod
    async def get_one(self, **kwargs: Any) -> ET: ...  # noqa: ANN401

    @abstractmethod
    async def update(self, uuid: UUID, **kwargs: Any) -> ET: ...  # noqa: ANN401
