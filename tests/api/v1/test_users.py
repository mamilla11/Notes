import requests

from .endpoints import (
    get_users_request,
    get_roles_request
)


def test_get_users_unauthorized(session: requests.Session):
    response = get_users_request(session)
    assert response.status_code == 401


def test_get_users_by_user(auth_user_session: requests.Session):
    session, _ = auth_user_session
    response = get_users_request(session)
    assert response.status_code == 403


def test_get_users_by_admin(auth_admin_session: requests.Session):
    session, user = auth_admin_session
    response = get_users_request(session)
    assert response.status_code == 200

    users = response.json()
    assert type(users) == list

    existing_user = list(filter(lambda x: x['id'] == user['id'], users))[0]
    assert existing_user['first_name'] == user['first_name']
    assert existing_user['last_name'] == user['last_name']
    assert existing_user['email'] == user['email']


def test_get_roles_unauthorized(session: requests.Session):
    response = get_roles_request(session)
    assert response.status_code == 401


def test_get_roles_by_user(auth_user_session: requests.Session):
    session, _ = auth_user_session
    response = get_roles_request(session)
    assert response.status_code == 403


def test_get_roles_by_admin(auth_admin_session: requests.Session):
    session, _ = auth_admin_session
    response = get_roles_request(session)
    assert response.status_code == 200

    roles = response.json()
    assert type(roles) == list
