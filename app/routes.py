from urllib.parse import urlsplit

from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_required, login_user
from flask_login import logout_user
import sqlalchemy as sa

from app import app, db
from app.forms import RegistrationForm
from app.forms import LoginForm
from app.models import User

# @app.route('/') maps the root URL (http://yourdomain.com/) to the function.
# @app.route('/index') maps the /index URL (http://yourdomain.com/index) to the same function.
@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    Renders the home page with a sample user and list of blog posts.

    The function prepares a mock user and a list of example posts,
    each containing an author and a body. It then renders the
    'index.html' template, passing the user and posts data to it.

    Returns:
        str: Rendered HTML of the index page using the specified template.
    """
    user = {'username': 'Isa'}
    posts = [
        {
            'author': {'username': 'Jim', 'email': 'jim@hotmail.com'},
            'body': 'What is Flask?'
        },
        {
            'author': {'username': 'John', 'email': 'john@hotmail.com'},
            'body': 'Flask is a micro web framework for Python.'
        },
        {
            'author': {'username': 'Alice'},
            'body': 'I love using Flask for web development!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login via GET and POST requests.

    GET: Renders the login form for the user.
    POST: Validates the submitted form. If valid, flashes a login confirmation message and redirects to the index page.

    Returns:
        A rendered login template on GET or form validation failure,
        or a redirect to the index page on successful login.
    """
    form = LoginForm()
    # Stops logged in user going to the login page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # What occurs when a login is submitted
    if form.validate_on_submit():
        # Checking the username and the password
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Logging in the user - Register the user as logged in
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# How to display the input by the user
# flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))


@app.route('/logout')
def logout():
    """
    Function to log the user out and return them to the homepage.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registers a new user.

    - Redirects authenticated users to the home page.
    - On GET: renders the registration form.
    - On valid POST: 
        - Creates a new user with the submitted username, email, and hashed password.
        - Persists the user to the database.
        - Flashes a success message and redirects to the login page.
    - On invalid POST or initial GET: re-renders the form with validation feedback.

    Returns:
        Response: redirect or rendered registration template.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulations, user {form.username.data} has now been registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)









