import re

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, session, abort, make_response
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import (
    Identity,
    AnonymousIdentity,
    identity_changed
)

from extensions import db, cache
from models import Role, User, user_schema


EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def signup(user):
    first_name = user.get('first_name')
    last_name = user.get('last_name')
    email = user.get('email')
    password = user.get('password')

    if not first_name or not last_name or not email or not password:
        abort(400, f'Not all data provided')

    if not re.match(EMAIL_PATTERN, email):
        abort(400, f'{email} is not a valid email')

    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user:
        abort(406, f'User with {email} email already exists')

    user['password'] = generate_password_hash(password, method='sha256')
    new_user = user_schema.load(user, session=db.session)

    db.session.add(new_user)
    db.session.commit()
    cache.delete('users')

    created_user = User.query.filter_by(id=new_user.id).first()
    role = Role.query.filter_by(name='user').first()

    if created_user is not None and role is not None:
        created_user.roles.append(role)
        db.session.commit()
    return user_schema.dump(created_user), 201


def login(credentials):
    email = credentials.get('email')
    password = credentials.get('password')

    existing_user = User.query.filter(User.email == email).one_or_none()

    if not existing_user or not check_password_hash(existing_user.password, password):
        abort(401, f'Invalid email or password')
    
    login_user(existing_user)
    identity_changed.send(
        current_app._get_current_object(),
        identity=Identity(existing_user.id)
    )

    return user_schema.dump(existing_user), 200


@login_required
def logout():
    email = current_user.email
    logout_user()

    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )
    return make_response(f'{email} is successfully logged out', 204)
