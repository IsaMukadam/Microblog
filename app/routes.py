from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
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

