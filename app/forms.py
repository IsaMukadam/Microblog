from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """
    Setting up a login form with the fields username, password, remember me and submit button.

    Attributes:
        username (StringField): Store users username
        password (PasswordField): Stores users password
        remember_me (BooleanField): Stores boolean remember me response
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

