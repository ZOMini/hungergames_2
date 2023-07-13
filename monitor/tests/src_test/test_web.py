import asyncio
from http import HTTPStatus as HTTP

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models_db import Link
from tests.settings import settings


@pytest.mark.asyncio
async def test_home_page(web_get_request, db_client: AsyncSession):
    if not await db_client.scalar(select(Link).filter(Link.domain == 'posredniksadovod_test')):
        await asyncio.sleep(0.5)
    body, headers, status = await web_get_request(settings.web_get_links)
    assert status[0] == HTTP.OK
    assert '<title>Links</title>' in body[0]
    assert 'http://abc.hostname.com/somethings/anything/qqq12345678/?sodfdme_key=som2e_value&amp;2wqeqwe=fsdgd2sf' in body[0]
    assert 'https://posredniksadovod_test.ru' in body[0]


@pytest.mark.asyncio
async def test_auth_page(web_get_request, db_client: AsyncSession):
    if not await db_client.scalar(select(Link).filter(Link.domain == 'posredniksadovod_test')):
        await asyncio.sleep(0.5)
    body, headers, status = await web_get_request(settings.web_get_links)
    assert status[0] == HTTP.OK
    assert 'Logs' not in body[0]
    