from abc import ABC
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseEntity(ABC, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    created_at: datetime

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __eq__(self, other: "BaseEntity") -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.uuid == other.uuid
