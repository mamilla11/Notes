import requests

from .endpoints import (
    get_notes_request,
    get_note_request,
    create_note_request,
    update_note_request,
    delete_note_request
)


def test_get_notes_unauthorized(session: requests.Session):
    response = get_notes_request(session)
    assert response.status_code == 401


def test_get_notes_by_user(auth_user_session: requests.Session):
    session, _ = auth_user_session

    # Get list of notes
    response = get_notes_request(session)
    assert response.status_code == 200

    notes = response.json()
    assert type(notes) == list
    # ------------------------------------------------------------ #

    # Get single note
    response = get_note_request(session, notes[0]['id'])
    assert response.status_code == 200

    note = response.json()
    assert notes[0] == note


def test_create_note_unauthorized(session: requests.Session):
    response = get_notes_request(session)
    assert response.status_code == 401


def test_create_note_by_user(auth_user_session: requests.Session):
    session, _ = auth_user_session

    # Create new note
    payload = {
        'content': 'My new note'
    }
    response = create_note_request(session, payload)
    assert response.status_code == 201

    created_note = response.json()
    assert created_note['content'] == payload['content']
    # ------------------------------------------------------------ #

    # Check that new note exists
    response = get_note_request(session, created_note['id'])
    assert response.status_code == 200

    received_note = response.json()
    assert created_note['content'] == received_note['content']
    # ------------------------------------------------------------ #

    # Delete new note
    response = delete_note_request(session, created_note['id'])
    assert response.status_code == 204


def test_update_note_unauthorized(session: requests.Session):
    note_id = 1
    payload = {
        'content': 'My new note'
    }
    response = update_note_request(session, note_id, payload)
    assert response.status_code == 401


def test_update_note_by_user(auth_user_session: requests.Session):
    session, _ = auth_user_session

    # Create new note
    payload = {
        'content': 'My another note'
    }
    response = create_note_request(session, payload)
    assert response.status_code == 201

    created_note = response.json()
    assert created_note['content'] == payload['content']
    # ------------------------------------------------------------ #

    # Update note
    edited_payload = {
        'content': 'Edited note'
    }
    response = update_note_request(session, created_note['id'], edited_payload)
    assert response.status_code == 200
    # ------------------------------------------------------------ #

    # Check that note is actually updated
    response = get_note_request(session, created_note['id'])
    assert response.status_code == 200

    updated_note = response.json()
    assert updated_note['content'] == edited_payload['content']
    # ------------------------------------------------------------ #

    # Delete note
    response = delete_note_request(session, created_note['id'])
    assert response.status_code == 204


def test_update_note_permissions(auth_user_session: requests.Session):
    session, user = auth_user_session

    # Get list of notes
    response = get_notes_request(session)
    assert response.status_code == 200
    notes = response.json()
    # ------------------------------------------------------------ #

    # Find a note created by someone else
    payload = {
        'content': 'My edited payload'
    }
    other_note = list(filter(lambda x: x['user_id'] != user['id'], notes))[0]
    # ------------------------------------------------------------ #

    # Check that user can not update other users notes
    response = update_note_request(session, other_note['id'], payload)
    assert response.status_code == 403


def test_delete_note_unauthorized(session: requests.Session):
    note_id = 1
    response = delete_note_request(session, note_id)
    assert response.status_code == 401


def test_delete_note_by_user(auth_user_session: requests.Session):
    session, _ = auth_user_session

    # Create new note
    payload = {
        'content': 'My another note'
    }
    response = create_note_request(session, payload)
    assert response.status_code == 201
    note_id = response.json()['id']
    # ------------------------------------------------------------ #

    # Delete note
    response = delete_note_request(session, note_id)
    assert response.status_code == 204
    # ------------------------------------------------------------ #

    # Check that note is actually deleted
    response = get_note_request(session, note_id)
    assert response.status_code == 404


def test_delete_note_permissions(auth_user_session: requests.Session):
    session, user = auth_user_session

    # Get list of notes
    response = get_notes_request(session)
    assert response.status_code == 200
    notes = response.json()

    # Find a note created by someone else
    other_note = list(filter(lambda x: x['user_id'] != user['id'], notes))[0]

    # Check that user can not delete other users notes
    response = delete_note_request(session, other_note['id'])
    assert response.status_code == 403
