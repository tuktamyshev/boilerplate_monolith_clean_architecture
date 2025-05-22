import uuid

from application.dtos.user import UserEmailDTO


class ReadUserDTO(UserEmailDTO):
    uuid: uuid.UUID
    is_active: bool
    is_superuser: bool
