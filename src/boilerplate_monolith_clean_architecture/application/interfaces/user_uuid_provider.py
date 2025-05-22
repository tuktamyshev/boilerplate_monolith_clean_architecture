from abc import ABC, abstractmethod
from uuid import UUID


class UserUUIDProviderInterface(ABC):
    @abstractmethod
    def get_current_user_uuid(self) -> UUID: ...
