import aiohttp
import pytest
import pytest_asyncio
from app import test_app
from flask import Flask

from core.app import login_manager
from db.models_db import User

user_jwt = ''


@pytest_asyncio.fixture
def web_get_request(ahttp_client: aiohttp.ClientSession):
    # Не используется, но оставил.
    async def inner(url: str, params: dict = {}, jwt: str = ''):
        if jwt:
            ahttp_client.headers['Authorization'] = f"Bearer {jwt}"
        async with ahttp_client.get(url, params=params) as response:
            body = await response.text(),
            headers = response.headers,
            status = response.status,
            return body, headers, status
    return inner


@pytest_asyncio.fixture
def app():
    app = test_app()
    app.config['WTF_CSRF_ENABLED'] = False
    app.testing = True
    return app


@pytest_asyncio.fixture
def test_client(app: Flask):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture()
def test_with_authenticated_user(app: Flask):
    @login_manager.request_loader
    def load_user_from_request(request):
        return User.query.first()


@pytest_asyncio.fixture
def runner(app: Flask):
    # Не используется.
    return app.test_cli_runner()
