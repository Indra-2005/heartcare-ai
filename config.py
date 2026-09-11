import os
import warnings
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class for the Flask application.
    Loads environment variables for secure database connections and secret keys.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        warnings.warn(
            "SECRET_KEY environment variable is not set. "
            "Sessions will be insecure. Set SECRET_KEY in your .env file.",
            RuntimeWarning,
            stacklevel=2,
        )

    # Fix Heroku's legacy 'postgres://' scheme — SQLAlchemy 1.4+ requires 'postgresql://'
    _db_url = os.environ.get('DATABASE_URL', '')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url or None

    SQLALCHEMY_TRACK_MODIFICATIONS = False