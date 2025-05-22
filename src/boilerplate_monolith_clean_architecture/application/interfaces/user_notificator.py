from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.value_objects.post_text import PostTextValueObject
from pydantic import BaseModel


class SendMessageToAnotherUserDTO(BaseModel):
    user_uuid_from: UUID
    text: str


class NotifyNewPostDTO(BaseModel):
    uuid: UUID
    user_uuid: UUID
    text: PostTextValueObject
    created_at: datetime


class NotifyUsersDTO(BaseModel):
    text: str


@dataclass(frozen=True)
class UserNotificatorInterface(ABC):
    @abstractmethod
    async def send_message_to_user_from_another_user(
        self, data: SendMessageToAnotherUserDTO, user_uuid: UUID
    ) -> None: ...

    @abstractmethod
    async def notify_new_post(self, data: NotifyNewPostDTO) -> None: ...

    @abstractmethod
    async def notify_users_about_something(self, data: NotifyUsersDTO) -> None: ...
