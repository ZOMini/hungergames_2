import asyncio

import aiohttp
import pytest_asyncio

user_jwt = ''


@pytest_asyncio.fixture
def make_get_request(ahttp_client: aiohttp.ClientSession):
    async def inner(url: str, params: dict = {}, jwt: str = ''):
        if jwt:
            ahttp_client.headers['Authorization'] = f"Bearer {jwt}"
        async with ahttp_client.get(url, params=params) as response:
            body = await response.json(),
            headers = response.headers,
            status = response.status,
            return body, headers, status
    return inner


@pytest_asyncio.fixture
def make_post_request(ahttp_client: aiohttp.ClientSession):
    async def inner(url: str, params: dict, json: dict, jwt=''):
        if jwt:
            ahttp_client.headers['Authorization'] = f"Bearer {jwt}"
        async with ahttp_client.post(url, params=params, json=json) as response:
            body = await response.json(),
            headers = response.headers,
            status = response.status,
            return body, headers, status
    return inner


@pytest_asyncio.fixture
def jwt_get_or_post():
    async def inner(post_body='', get: bool = True):
        if not get:
            global user_jwt
            user_jwt = post_body
        if not user_jwt:
            await asyncio.sleep(0.4)
        return user_jwt
    return inner


@pytest_asyncio.fixture
def make_post_request_with_file(ahttp_client: aiohttp.ClientSession):
    async def inner(url: str, params: dict = {}, jwt='', file=''):
        if jwt:
            ahttp_client.headers['Authorization'] = f'Bearer {jwt}'
        files = {'file': open('./tests/testdata/urls.zip', 'rb')}
        async with ahttp_client.post(url, params=params, data=files) as response:
            body = await response.json(),
            headers = response.headers,
            status = response.status,
            return body, headers, status
    return inner
