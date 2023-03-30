import os

from dotenv import load_dotenv


load_dotenv()


CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
