import os

import pytest
import requests
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from .endpoints import (
    login_request,
    logout_request
)


load_dotenv()


DLS = {
    'dbname':   os.environ.get('POSTGRES_DB'),
    'user':     os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host':     os.environ.get('POSTGRES_HOST', 'localhost'),
    'port':     os.environ.get('POSTGRES_PORT', 5432)
}


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    '''
    Fill database with test data
    '''
    with psycopg2.connect(**DLS, cursor_factory=DictCursor) as conn:
        with conn.cursor() as cursor:
            cursor.execute(open('cleanup.sql', 'r').read())
            cursor.execute(open('schema.sql', 'r').read())
            conn.commit()
            yield
            cursor.execute(open('cleanup.sql', 'r').read())
            conn.commit()


@pytest.fixture(scope='session')
def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope='function')
def auth_user_session(session):
    payload = {
        'email': 'user@mail.com',
        'password': 'qwerty'
    }
    response = login_request(session, payload)
    assert response.status_code == 200

    yield session, response.json()

    response = logout_request(session)
    assert response.status_code == 204


@pytest.fixture(scope='function')
def auth_admin_session(session):
    payload = {
        'email': 'admin@mail.com',
        'password': 'qwerty'
    }
    response = login_request(session, payload)
    assert response.status_code == 200

    yield session, response.json()

    response = logout_request(session)
    assert response.status_code == 204
