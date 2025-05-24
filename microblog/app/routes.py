from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return '''
    <html>
        <head>
            <title>Microblog</title>
        </head>
        <body>
            <h1>Hello, {}</h1>
            <h2>Posts:</h2>
            <ul>
                {}
            </ul>
        </body>
    </html>
    '''.format(user['username'], ''.join(f'<li>{post["author"]["username"]}: {post["body"]}</li>' for post in posts))