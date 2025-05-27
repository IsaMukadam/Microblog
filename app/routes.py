# Importing the render template and the app
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)




