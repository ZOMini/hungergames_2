import asyncio
from http import HTTPStatus as HTTP

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models_db import Link
from tests.settings import settings


@pytest.mark.asyncio
async def test_links_page(web_get_request, db_client: AsyncSession):
    if not await db_client.scalar(select(Link).filter(Link.domain == 'posredniksadovod_test')):
        await asyncio.sleep(0.5)
    body, headers, status = await web_get_request(settings.web_get_links)
    assert status[0] == HTTP.OK
    assert '<title>Links</title>' in body[0]
    assert 'Create account' in body[0]
    assert 'Available' in body[0]
    assert 'Domain name' in body[0]
    assert 'Domain zone' in body[0]


@pytest.mark.asyncio
async def test_register_page(web_get_request, db_client: AsyncSession):
    if not await db_client.scalar(select(Link).filter(Link.domain == 'posredniksadovod_test')):
        await asyncio.sleep(0.5)
    body, headers, status = await web_get_request(settings.web_get_register)
    assert status[0] == HTTP.OK
    assert 'Create an account' in body[0]
    assert 'Name' in body[0]
    assert 'Email' in body[0]
    assert 'Password' in body[0]
    assert 'Confirm' in body[0]
