from http import HTTPStatus as HTTP

import pytest

from tests.settings import settings
from tests.testdata import api_data


@pytest.mark.parametrize(
    'body_data, expected_answer',
    [({'body': api_data.user_create_data},
      {'status': HTTP.CREATED, 'json': 'User created. Login is email.'}, ),])
@pytest.mark.asyncio
async def test_auth_user_create(make_post_request, body_data, expected_answer, db_get_user_by_name):
    """API.Auth.Создаем и проверяем создание пользователя."""
    body, headers, status = await make_post_request(
        settings.auth_create_url, params={}, json=body_data['body'])
    user = await db_get_user_by_name(body_data['body']['name'])
    assert status[0] == expected_answer['status']
    assert body[0] == expected_answer['json']


@pytest.mark.parametrize(
    'body_data, expected_answer',
    [({'body': api_data.user_login_data},
      {'status': HTTP.CREATED}, ),])
@pytest.mark.asyncio
async def test_auth_login(make_post_request, jwt_get_or_post, body_data, expected_answer):
    """API.Auth. Проверяем логин."""
    body, headers, status = await make_post_request(
        settings.auth_login_url, params={}, json=body_data['body'])
    assert status[0] == expected_answer['status']
    await jwt_get_or_post(post_body=body[0]['access_token'], get=False)


@pytest.mark.parametrize(
    'body_data, expected_answer',
    [({'body': api_data.monitor_url_post_data, 'query': api_data.monitor_url_get_data},
      {'status': HTTP.CREATED, 'json': api_data.monitor_url_post_response, 'status_get': HTTP.OK}, ), ])
@pytest.mark.asyncio
async def test_monitor_post_and_get_url(make_post_request, make_get_request, make_post_request_with_file, jwt_get_or_post, body_data, expected_answer):
    """API.Monitor. Проверяем одиночный пост урла.
    Потом постим картинку для него.
    Затем делаем get запрос и проверяем все ли верно прилетает."""
    jwt = await jwt_get_or_post()
    body, headers, status = await make_post_request(
        settings.monitor_post_url, params={}, json=body_data['body'], jwt=jwt)
    body_data['query']['id'] = body[0]['id']
    del body[0]['id']
    assert status[0] == expected_answer['status']
    assert body[0] == expected_answer['json']
    _id = body_data['query']['id']
    body, headers, status = await make_post_request_with_file(f'{settings.monitor_post_image}/{_id}', jwt=jwt, file='./tests/testdata/image.jpg')
    assert status[0] == expected_answer['status_get']
    assert body[0] == 'File appended/updated.'
    body, headers, status = await make_get_request(settings.monitor_get_urls, params=body_data['query'], jwt=jwt)
    assert status[0] == expected_answer['status_get']
    assert body[0][0]['url'] == body_data['body']['url']


@pytest.mark.parametrize(
    'body_data, expected_answer',
    [({},
      {'status': HTTP.ACCEPTED, 'json': {'successfully': 1}}, ),])
@pytest.mark.asyncio
async def test_monitor_post_urls(make_post_request_with_file, jwt_get_or_post, body_data, expected_answer):
    """API.Monitor. Проверяем пост из zip файла."""
    jwt = await jwt_get_or_post()
    body, headers, status = await make_post_request_with_file(
        settings.monitor_post_urls, params={}, jwt=jwt, file='./tests/testdata/urls.zip')
    assert status[0] == expected_answer['status']
    assert body[0] == expected_answer['json']


@pytest.mark.asyncio
async def test_monitor_get_logs(make_get_request, jwt_get_or_post):
    """API.Monitor. Простенький тест логов, прилетает ли."""
    jwt = await jwt_get_or_post()
    body, headers, status = await make_get_request(
        settings.monitor_get_logs, params={}, jwt=jwt)
    assert status[0] == HTTP.OK
    assert isinstance(body[0], list)

