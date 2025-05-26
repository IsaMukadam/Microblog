# Importing needed libs 
from flask import Flask
from config import Config
from app.forms import LoginForm

# Creating an instance of the flask class
app = Flask(__name__)
# Updating the instance app with the values from the config class
app.config.from_object(Config)

# Importing routes
from app import routes
