import asyncio

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models_db import Link
from services import worker_service
from tests.testdata import worker_data


@pytest.mark.asyncio
async def test_worker(db_client: AsyncSession):
    """Worker. Простенький тест воркера, штатно ли работает."""
    if not await db_client.scalar(select(Link).filter(Link.domain == 'posredniksadovod_test')):
        await asyncio.sleep(0.5)
    result = await worker_service.run_works_async()
    assert worker_data.worker_result == result
