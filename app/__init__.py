from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Importing routes


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

# Import routes at the end, after app and db are ready
from app import routes
from app import models

# Example user input
# u = User(username='susan', email='susan@example.com')