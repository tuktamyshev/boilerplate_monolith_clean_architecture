from uuid import UUID

from domain.entities.user import UserEntity
from domain.value_objects.email import EmailValueObject


def test_user_create_success():
    email = EmailValueObject("test@example.com")
    hashed_password = "hashed_pwd"

    user = UserEntity.create(email=email, hashed_password=hashed_password)

    assert isinstance(user.uuid, UUID)
    assert user.email == email
    assert user.hashed_password == hashed_password
    assert user.is_active is True
    assert user.is_superuser is False
    assert user.is_verified is False
    assert user.created_at is not None
