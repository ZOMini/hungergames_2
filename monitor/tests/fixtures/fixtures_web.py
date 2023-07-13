import aiohttp
import pytest_asyncio

user_jwt = ''


@pytest_asyncio.fixture
def web_get_request(ahttp_client: aiohttp.ClientSession):
    async def inner(url: str, params: dict = {}, jwt: str = ''):
        if jwt:
            ahttp_client.headers['Authorization'] = f"Bearer {jwt}"
        async with ahttp_client.get(url, params=params) as response:
            body = await response.text(),
            headers = response.headers,
            status = response.status,
            return body, headers, status
    return inner
