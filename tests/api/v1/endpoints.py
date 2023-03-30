import os

import requests
from dotenv import load_dotenv


load_dotenv()


API_ENDPOINT = os.environ.get('API_ENDPOINT')


def signup_request(session: requests.Session, payload: dict):
    return session.post(f'{API_ENDPOINT}/signup', json=payload)


def login_request(session: requests.Session, payload: dict):
    return session.post(f'{API_ENDPOINT}/login', json=payload)


def logout_request(session: requests.Session):
    return session.post(f'{API_ENDPOINT}/logout')


def get_notes_request(session: requests.Session):
    return session.get(f'{API_ENDPOINT}/notes')


def get_note_request(session: requests.Session, note_id: int):
    return session.get(f'{API_ENDPOINT}/notes/{note_id}')


def create_note_request(session: requests.Session, payload: dict):
    return session.post(f'{API_ENDPOINT}/notes', json=payload)


def update_note_request(session: requests.Session, note_id: int, payload: dict):
    return session.put(f'{API_ENDPOINT}/notes/{note_id}', json=payload)


def delete_note_request(session: requests.Session, note_id: int):
    return session.delete(f'{API_ENDPOINT}/notes/{note_id}')


def get_users_request(session: requests.Session):
    return session.get(f'{API_ENDPOINT}/users')


def get_roles_request(session: requests.Session):
    return session.get(f'{API_ENDPOINT}/roles')
