from urllib.parse import urlsplit
from datetime import datetime, timezone

from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_required, login_user
from flask_login import logout_user
import sqlalchemy as sa

from app import app, db
from app.forms import RegistrationForm
from app.forms import LoginForm
from app.forms import EmptyForm
from app.models import User
from app.forms import EditProfileForm

# @app.route('/') maps the root URL (http://yourdomain.com/) to the function.
# @app.route('/index') maps the /index URL (http://yourdomain.com/index) to the same function.
@app.route('/')
@app.route('/index')
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

@app.route('/user/<username>')
@login_required
def user(username):
    """
    Displays the users profile page.

    Args:
        username (str): The username of the user whose page is being displayed
        form (FlaskForm): An instance of the EmptyForm class for follow/unfollow actions.
        posts (list): A list of example posts authored by the user.
    Return:
        Renders the user.html template with the user's information, posts, and form.
    """
    form = EmptyForm()
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts, form=form)


@app.before_request
def before_request():
    """
    Gets the last seen time for a user to display on their profile page.
    Stores this in the last_seen parameter of the User in the db
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Allows a logged-in user to view and edit their profile information.

    On GET requests, it pre-populates the form with the current user's profile data.
    On POST requests, it updates the user's profile if the submitted form is valid.

    Returns:
        A rendered HTML template for the edit profile page, or redirects back to 
        the same page with a success message after a successful update.
    """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    """
    Allows the current user to follow another user.

    Args:
        username (str): The username of the user to follow.
    Returns:
        Redirects to the followed user's profile page on success,
        or back to the index page if the form validation fails.

    """
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    """
    Allows the current user to unfollow another user.

    Args:
        username (str): The username of the user to unfollow.
    Returns:
        Redirects to the unfollowed user's profile page on success,
        or back to the index page if the form validation fails.

    """
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You have unfollowed {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    






