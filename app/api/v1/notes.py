from flask import abort, make_response
from sqlalchemy import desc
from flask_login import login_required, current_user

from extensions import db, cache
from permissions import EditNotePermission
from models import (
    Note,
    note_schema,
    notes_schema
)


@login_required
@cache.cached(timeout=60, key_prefix='notes')
def read_all():
    notes = Note.query.order_by(desc(Note.modified))
    return notes_schema.dump(notes)


@login_required
def read_one(note_id):
    note = Note.query.get(note_id)

    if not note:
        abort(404, f'Note with id {note_id} not found')

    return note_schema.dump(note)


@login_required
def create(note):
    note['user_id'] = current_user.id
    new_note = note_schema.load(note, session=db.session)
    db.session.add(new_note)
    db.session.commit()
    cache.delete('notes')
    return note_schema.dump(new_note), 201


@login_required
def update(note_id, note):
    existing_note = Note.query.get(note_id)

    if not existing_note:
        abort(404, f'Note with ID {note_id} not found')
    
    permission = EditNotePermission(note_id)

    if not permission.can():
        abort(403, f'Not authorized to edit note with ID {note_id}')

    update_note = note_schema.load(note, session=db.session)
    existing_note.content = update_note.content
    db.session.merge(existing_note)
    db.session.commit()
    cache.delete('notes')
    return note_schema.dump(existing_note), 200


@login_required
def delete(note_id):
    existing_note = Note.query.get(note_id)

    if not existing_note:
        abort(404, f'Note with ID {note_id} not found')

    if not EditNotePermission(note_id).can():
        abort(403, f'Not authorized to delete note with ID {note_id}')

    db.session.delete(existing_note)
    db.session.commit()
    return make_response(f'Note {note_id} is successfully deleted', 204)
