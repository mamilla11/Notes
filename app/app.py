import os
import pathlib

import connexion
from dotenv import load_dotenv

from models import User
from extensions import init_extensions, login_manager
from permissions import init_permissions
from flask import request, render_template


load_dotenv()


BASE_DIR = pathlib.Path(__file__).parent.resolve()

# List of all APIs specifications
specifications = [
    os.path.join(BASE_DIR, 'api', 'v1', 'swagger.yml'),
]

# Create an app
connex_app = connexion.App(__name__)

# Add all API specifications to the app
for spec in specifications:
    connex_app.add_api(
        specification=os.path.join(spec),
        strict_validation=True,
        validate_responses=True
    )

# Setup configuration
app = connex_app.app
app.config.from_pyfile('config.py')

# Initialize extensions
init_extensions(app)
init_permissions(app)


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


@connex_app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
