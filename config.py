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
                          
        SQLALCHEMY_DATABASE_URI (str): Database connection string for SQLAlchemy.
                                    Loaded from 'DATABASE_URL' environment variable,
                                    or defaults to SQLite database in app.db file.
        
        MAIL_SERVER (str): SMTP server hostname for sending emails.
                        Loaded from 'MAIL_SERVER' environment variable.
        
        MAIL_PORT (int): SMTP server port number for email sending.
                        Loaded from 'MAIL_PORT' environment variable,
                        or defaults to 25 if not set.
        
        MAIL_USE_TLS (bool): Whether to use TLS encryption for email sending.
                            Set to True if 'MAIL_USE_TLS' environment variable exists,
                            False otherwise.
        
        MAIL_USERNAME (str): Username for SMTP server authentication.
                            Loaded from 'MAIL_USERNAME' environment variable.
        
        MAIL_PASSWORD (str): Password for SMTP server authentication.
                            Loaded from 'MAIL_PASSWORD' environment variable.
        
        ADMINS (list): List of administrator email addresses for error notifications.
                    Contains email addresses that will receive error reports
                    in production environment.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'isa-secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Handle emailing errors in production application
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']