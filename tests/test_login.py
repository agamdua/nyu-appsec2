import pytest

from app import app


@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    testing_client = flask_app.test_client()

    yield testing_client


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 302


def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
