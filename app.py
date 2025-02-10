from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure the instance folder exists
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    """Initialize the database and create tables"""
    try:
        with app.app_context():
            db.create_all()
            print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        return str(e)
    return None
