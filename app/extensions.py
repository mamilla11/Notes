from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_principal import Principal


# Create global for extensions
db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
principal = Principal()


def init_extensions(app: Flask):
    # Initialize extensions with the Flask app
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
