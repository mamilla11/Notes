from collections import namedtuple
from functools import partial

from flask import Flask
from flask_login import current_user
from flask_principal import (
    Permission,
    UserNeed,
    RoleNeed,
    identity_loaded
)


admin_permission = Permission(RoleNeed('admin'))

NoteNeed = namedtuple('blog_post', ['method', 'value'])
EditNoteNeed = partial(NoteNeed, 'edit')

# This permission allows a note update only by it's author
class EditNotePermission(Permission):
    def __init__(self, note_id):
        need = EditNoteNeed(str(note_id))
        super(EditNotePermission, self).__init__(need)


def init_permissions(app: Flask):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
        
        if hasattr(current_user, 'notes'):
            for note in current_user.notes:
                identity.provides.add(EditNoteNeed(str(note.id)))
