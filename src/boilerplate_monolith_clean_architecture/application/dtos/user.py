from typing import Any

from domain.value_objects.email import EmailValueObject
from pydantic import BaseModel, ConfigDict


class UserEmailDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailValueObject

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        super().__init__(**data)
        self.email = self.email.lower()
