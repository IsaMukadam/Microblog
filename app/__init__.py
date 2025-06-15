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
login = LoginManager(app)
login.login_view = 'login'

# Importing routes
from app import routes, models

# Example user input
# u = User(username='susan', email='susan@example.com')
