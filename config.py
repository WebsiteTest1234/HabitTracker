import os

class Config:
    # Use absolute path for SQLite database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "habits.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False