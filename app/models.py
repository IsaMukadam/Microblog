from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    """
    Creating a model which represents users.

    Parameters:
    id: A unique id as the primary key for each user.
    username: a username up to a 64 character string.
    email: an email up to 120 character string.
    password_hash: a optional string value which is up to 256 character string in the form of password hashes.

    Functions:
    __repr__: Return a string representation of the User object for debugging purposes.
    The format is <User username>, where 'username' is the value of the user's username attribute.
    This representation is intended to be unambiguous and useful for developers.
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    

class Post(db.Model):
    """
    Creating a model for a user post.

    Parameters:
    id: primary key and unique id for each post.
    body: text body for the post.
    timestamp: the time that it was posted.
    user_id: the id of the user who posted (FK of User Table).
    author: Represents the relationship between the user and posts.
    
    Functions:
    __repr__: Displays the post body.
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    


# Querying the DB for specific values using .select and .where
# >>> query = sa.select(User).where(User.username.like('s%'))
# >>> db.session.scalars(query).all()
