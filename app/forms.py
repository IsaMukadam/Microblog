from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms import TextAreaField

import sqlalchemy as sa

from app import db
from app.models import User

class LoginForm(FlaskForm):
    """
    A user login form built with Flask-WTF.

    Includes fields for username, password, a 'remember me' option, and a submit button.

    Attributes:
        username (StringField): Required field for the user's username.
        password (PasswordField): Required field for the user's password.
        remember_me (BooleanField): Optional checkbox to keep the user logged in.
        submit (SubmitField): Button to submit the form.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    A user registration form built using Flask-WTF

    Includes fields for username, email, password, password1, and a submit button.

    Attributes:
        username (StringField): Required field for user's username.
        email (StringField): Required field for the user's email.
        password (PasswordField): Required field for the user's password.
        password1 (PasswordField): Required field to confirm user's password in password field.
        submit (SubmitField): Button to submit the form.

    Methods:
        validate_username(): Ensures the username used doesn't already exist.
        validate_email(): Ensures the email used doesn't already exist.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    """
    A form to edit the user profile page.

    Attributes:
        username (StringField): Required field for user's username.
        about_me (TextAreaField): The about me section for the user.

    Methods:
        ...
    """
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        """
        Initialise the form with the user's original username.

        Args:
            original_username (str): The current username of the user before editing.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments passed to the parent class.
        """
        super().__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        """
        Validate that the username is not already taken by another user.

        Args:
            username: The form field data containing the username to validate.

        Raises:
            ValidationError: If the username is already used by a different user.
        """
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
            

class EmptyForm(FlaskForm):
    """
    A simple form with only a submit button.

    Used for actions that don't require additional input, such as following or unfollowing a user.

    Attributes:
        submit (SubmitField): Button to submit the form.
    """
    submit = SubmitField('Submit')