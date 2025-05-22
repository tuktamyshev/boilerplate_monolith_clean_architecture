import pytest

from domain.exceptions.access import AccessException
from domain.services.access import AccessService
from tests.factories.entities import PostEntityFactory, UserEntityFactory


def test_check_is_admin_allows_superuser(access_service: AccessService):
    user = UserEntityFactory(is_superuser=True)

    access_service.check_is_admin(user)


def test_check_is_admin_denies_non_superuser(access_service: AccessService):
    user = UserEntityFactory(is_superuser=False)

    with pytest.raises(AccessException):
        access_service.check_is_admin(user)


def test_check_is_owner_allows_owner(access_service: AccessService):
    user = UserEntityFactory()
    post_entity = PostEntityFactory(user_uuid=user.uuid)

    access_service.check_is_owner(user.uuid, post_entity)


def test_check_is_owner_denies_non_owner(access_service: AccessService):
    user = UserEntityFactory()
    post_entity = PostEntityFactory()
    with pytest.raises(AccessException):
        access_service.check_is_owner(user.uuid, post_entity)
