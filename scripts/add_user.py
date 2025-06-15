from app import app, db
from app.models import User

with app.app_context():
    user = User(username="jane", email="jane@example.com")
    user.set_password("mypassword")
    db.session.add(user)
    db.session.commit()
    print("User added successfully!")