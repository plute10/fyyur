import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgres://1003867@localhost:5432/fyyur'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = 'this is jinhee chung'
