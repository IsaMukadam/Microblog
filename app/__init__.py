# Importing needed libs 
from flask import Flask
from config import Config
from app.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Creating an instance of the flask class
app = Flask(__name__)
# Updating the instance app with the values from the config class
app.config.from_object(Config)
# Creating a db instance using SQLAlchemy
db = SQLAlchemy(app)
# Setting up migration engine
migrate = Migrate(app, db)

# Importing routes
from app import routes, models


# u = User(username='susan', email='susan@example.com')