import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
# from app.forms import LoginForm


# Creating an instance of the flask class
app = Flask(__name__)
# Updating the instance app with the values from the config class
app.config.from_object(Config)


# Creating a db instance using SQLAlchemy
db = SQLAlchemy(app)
# Setting up migration engine
migrate = Migrate(app, db)


# Setting up the Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
# Load user
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# Example user input
# u = User(username='susan', email='susan@example.com')

# If application is not in debug mode
if not app.debug:
    
    # Configure email error logging for production environment
    # Only runs when debug mode is disabled and MAIL_SERVER is configured
    # Sends error notifications to admins via SMTP when exceptions occur
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure
            )
        mail_handler.setLevel(logging.ERROR)
        print("📧 Email error logging setup is active")
        app.logger.addHandler(mail_handler)

    # Configure a file based error logging system using a RotatingFileHandler
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog')

# Import routes at the end, after app and db are ready and errors
from app import routes, models, errors