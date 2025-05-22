import pytest

from domain.services.access import AccessService


@pytest.fixture(scope="session")
async def access_service() -> AccessService:
    return AccessService()
