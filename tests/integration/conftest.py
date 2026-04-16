from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.main import app
from tests.conftest import test_session_factory


@pytest_asyncio.fixture
async def integration_client(
    setup_database,
) -> AsyncGenerator[tuple[AsyncClient, AsyncSession], None]:
    async with test_session_factory() as session:
        async with session.begin():
            async def _override_session() -> AsyncGenerator[AsyncSession, None]:
                yield session

            app.dependency_overrides[get_db_session] = _override_session

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                yield client, session

            app.dependency_overrides.clear()
            await session.rollback()
