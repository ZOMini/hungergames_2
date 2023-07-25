from http import HTTPStatus as Http

import pytest
from flask.testing import FlaskClient

from core.logger import console_logger
from tests.testdata import web_data


def test_register(test_client: FlaskClient):
    response = test_client.post(web_data.register_uri, data={'name': 'testuser2', 'email': 'test2@ya.ru', 'password': 'testpass', 'confirm': 'testpass'})
    assert Http.FOUND == response.status_code
    assert b'<title>Redirecting...</title>' in response.data


def test_login(test_client: FlaskClient):
    response = test_client.post(web_data.links_uri, data={'email': 'test2@ya.ru', 'password': 'testpass', 'action': 'submit'})
    assert Http.FOUND == response.status_code
    assert b'<title>Redirecting...</title>' in response.data


@pytest.mark.parametrize(
    'uri, status',
    [({'uri': web_data.links_uri, }, {'status': Http.OK, 'data': b'<title>Links</title>'}),
     ({'uri': web_data.events_uri, }, {'status': Http.FOUND, 'data': b'<a href="/web/links">/web/links</a>'}),
     ({'uri': web_data.logs_uri, }, {'status': Http.FOUND, 'data': b'<a href="/web/links">/web/links</a>'}),
     ({'uri': web_data.new_links_uri, }, {'status': Http.FOUND, 'data': b'<a href="/web/links">/web/links</a>'}),
     ({'uri': web_data.upload_image_uri, }, {'status': Http.FOUND, 'data': b'<a href="/web/links">/web/links</a>'}),
     ]
)
def test_pages_wo_auth(test_client: FlaskClient, uri, status):
    '''Тестируем недоступность страниц, если неавторизован.'''
    response = test_client.get(uri['uri'])
    # console_logger.error(response.data)
    assert status['status'] == response.status_code
    assert status['data'] in response.data


@pytest.mark.parametrize(
    'uri, status',
    [({'uri': web_data.links_uri, }, {'status': Http.OK, 'data': b'<title>Links</title>'}),
     ({'uri': web_data.events_uri, }, {'status': Http.OK, 'data': b'<meta name="turbolinks-visit-control"'}),
     ({'uri': web_data.logs_uri, }, {'status': Http.OK, 'data': b'PDF Download</a></button>'}),
     ({'uri': web_data.new_links_uri, }, {'status': Http.OK, 'data': b'<input class="form-control" id="file" name="file" required type="file">'}),
     ({'uri': web_data.upload_image_uri, }, {'status': Http.OK, 'data': b'<input class="form-control" id="file" name="file" required type="file">'}),
     ]
)
def test_pages_with_auth(test_client: FlaskClient, test_with_authenticated_user, uri, status):
    '''Тестируем доступность страниц, если авторизован.'''
    response = test_client.get(uri['uri'])
    # console_logger.error(response.data)
    assert status['status'] == response.status_code
    assert status['data'] in response.data
