import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Base configuration class for the Flask application.
    Loads environment variables for secure database connections and secret keys.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False