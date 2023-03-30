from flask import abort
from flask_login import login_required

from permissions import admin_permission
from models import (
    User,
    Role,
    users_schema,
    roles_schema
)


@login_required
def read_all():
    if not admin_permission.can():
        abort(403, f'Not authorized to get user information')

    users = User.query.all()
    return users_schema.dump(users)


@login_required
def get_roles():
    if not admin_permission.can():
        abort(403, f'Not authorized to get user information')

    roles = Role.query.all()
    return roles_schema.dump(roles)
