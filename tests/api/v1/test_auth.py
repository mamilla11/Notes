import pytest
import requests

from .endpoints import (
    signup_request,
    login_request,
    logout_request
)


def test_singup(session: requests.Session):
    # Signup new user
    payload = {
        'first_name': 'Jhon',
        'last_name' : 'Doe',
        'email'     : 'jhondoe@mail.com',
        'password'  : 'passdoe'
    }
    response = signup_request(session, payload)
    assert response.status_code == 201
    # ----------------------------------------------- #

    # Check that it is impossible to dublicate a user
    response = signup_request(session, payload)
    assert response.status_code == 406
    # ----------------------------------------------- #

    # Check that it is impossible to dublicate an email
    payload.update({
        'first_name': 'Anna',
        'last_name': 'Toe',
        'password': 'passtoe'
    })
    response = signup_request(session, payload)
    assert response.status_code == 406
    # ----------------------------------------------- #

    # Check that it is impossible to pass wrong email
    payload.update({
        'email': 'annatoe@mailcom'
    })
    response = signup_request(session, payload)
    assert response.status_code == 400


@pytest.mark.parametrize(
    'payload',
    [
        # Payload field is empty
        ({'first_name': ''    , 'last_name': 'Toe', 'email': 'annatoe@mail.com', 'password': 'passtoe'}),
        ({'first_name': 'Anna', 'last_name': ''   , 'email': 'annatoe@mail.com', 'password': 'passtoe'}),
        ({'first_name': 'Anna', 'last_name': 'Toe', 'email': ''                , 'password': 'passtoe'}),
        ({'first_name': 'Anna', 'last_name': 'Toe', 'email': 'annatoe@mail.com', 'password': ''}),

        # Payload field is missing
        ({                      'last_name': 'Toe', 'email': 'annatoe@mail.com', 'password': 'passtoe'}),
        ({'first_name': 'Anna',                     'email': 'annatoe@mail.com', 'password': 'passtoe'}),
        ({'first_name': 'Anna', 'last_name': 'Toe',                              'password': 'passtoe'}),
        ({'first_name': 'Anna', 'last_name': 'Toe', 'email': 'annatoe@mail.com',                      }),
    ]
)
def test_signup_payload(session: requests.Session, payload: dict):
    response = signup_request(session, payload)
    assert response.status_code == 400


def test_login(session: requests.Session):
    # Existing user can login
    payload = {
        'email': 'jhondoe@mail.com',
        'password': 'passdoe'
    }
    response = login_request(session, payload)
    assert response.status_code == 200
    # ----------------------------------------------- #
    
    # Unknown user can not login
    payload = {
        'email': 'annatoe@mail.com',
        'password': 'passyoe'
    }
    response = login_request(session, payload)
    assert response.status_code == 401


def test_logout(session):
    # Login user
    payload = {
        'email': 'jhondoe@mail.com',
        'password': 'passdoe'
    }
    response = login_request(session, payload)
    assert response.status_code == 200
    # ----------------------------------------------- #

    # Logout user
    response = logout_request(session)
    assert response.status_code == 204
    # ----------------------------------------------- #

    # Logout again
    response = logout_request(session)
    assert response.status_code == 401
    # ----------------------------------------------- #

