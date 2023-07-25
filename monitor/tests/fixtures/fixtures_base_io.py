import asyncio
from typing import AsyncGenerator

import aiohttp
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from tests.settings import settings


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def db_client():
    engine = create_async_engine(settings.pg_async_url, query_cache_size=0)
    async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=True)
    session = async_session()
    yield session
    session.close()


@pytest_asyncio.fixture(scope="session")
async def ahttp_client() -> AsyncGenerator[aiohttp.ClientSession, None]:
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
        limit=35, loop=asyncio.get_event_loop()))
    yield session
    await session.close()
