# Importing the os package
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        SECRET_KEY (str): A secret key used for securing sessions and cookies.
                          It is loaded from the environment variable 'SECRET_KEY',
                          or defaults to 'isa-secret-key' if not set.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'isa-secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')