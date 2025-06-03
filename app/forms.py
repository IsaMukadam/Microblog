from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """
    Login form using Flask-WTF.

    Defines the fields required for user authentication, including username, password, 
    an optional 'remember me' checkbox, and a submit button.

    Attributes:
        username (StringField): Field for entering the user's username. Required.
        password (PasswordField): Field for entering the user's password. Required.
        remember_me (BooleanField): Checkbox to indicate whether the user should remain logged in.
        submit (SubmitField): Button to submit the login form.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

