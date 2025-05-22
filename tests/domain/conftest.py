from typing import AsyncGenerator

import pytest
from dishka import AsyncContainer, make_async_container

from domain.services.access import AccessService
from main.di import DomainServiceProvider

@pytest.fixture(scope="session")
async def access_service() -> AccessService:
    return AccessService()
