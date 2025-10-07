import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    """
    Test case for the User model.

    This class sets up a test environment for the User model, including
    creating an in-memory SQLite database, and provides methods to test
    user creation, password hashing, and other user-related functionalities.

    Attributes:
        app_context: The application context for the Flask app.
        db: The SQLAlchemy database instance.
        User: The User model class.
        Post: The Post model class.

    Methods:
        setUp(): Sets up the test environment before each test method.
        tearDown(): Cleans up the test environment after each test method.
        test_password_hashing(): Tests the password hashing and verification methods.
        test_avatar(): Tests the avatar URL generation method.
        test_follow(): Tests the follow and unfollow methods, as well as follower/following counts.
        test_follow_posts(): Tests the retrieval of posts from followed users.
    """
    
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
        
    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        following = db.session.execute(u1.following.select()).scalars().all()
        followers = db.session.execute(u1.followers.select()).scalars().all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)
        u1_following = db.session.execute(u1.following.select()).scalars().all()
        u2_followers = db.session.execute(u2.followers.select()).scalars().all()
        self.assertEqual(u1_following[0].username, 'susan')
        self.assertEqual(u2_followers[0].username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

    def test_follow_posts(self):
        # Create four users
        u1 = User(username='john', email = 'john@example.com')
        u2 = User(username='susan', email = 'susan@example.com')
        u3 = User(username='mary', email = 'mary@example.com')
        u4 = User(username='david', email = 'david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # Create four posts with specific timestamps
        now = datetime.now(timezone.utc)
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                    timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                    timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                    timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # Set up follower relationships
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # Verify the followed posts for each user
        f1 = db.session.execute(u1.following_posts()).scalars().all()
        f2 = db.session.execute(u2.following_posts()).scalars().all()
        f3 = db.session.execute(u3.following_posts()).scalars().all()
        f4 = db.session.execute(u4.following_posts()).scalars().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)