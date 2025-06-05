from typing import Optional
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin

from app import db
from app import login


class User(UserMixin, db.Model):
    """
    An SQLAlchemy model representing a user in the system.

    Attributes:
        id (int): Unique primary key for each user.
        username (str): A unique username (max 64 characters).
        email (str): A unique email address (max 120 characters).
        password_hash (str, optional): The hashed password (max 256 characters).
        posts (List[Post]): A one-to-many relationship to posts authored by the user.

    Methods:
        __repr__(): Returns a readable string representation of the user (e.g., <User johndoe>).
        set_password(password): Hashes and stores the provided password.
        check_password(password): Verifies a provided password against the stored hash.
        load_user(id): Returns the user with the id specified.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(
        sa.String(64),
        index=True,
        unique=True
    )

    email: so.Mapped[str] = so.mapped_column(
        sa.String(120),
        index=True,
        unique=True
    )

    password_hash: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256)
    )

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User,int(id))


class Post(db.Model):
    """
    An SQLAlchemy model representing a user post.

    Attributes:
    id (int): Unique primary key for each post.
    body (str): The content of the post, limited to 140 characters.
    timestamp (datetime): The UTC datetime when the post was created.
    user_id (int): Foreign key referencing the user who authored the post.
    author (User): Relationship to the User model that owns the post.

    Methods:
        __repr__(): Returns a concise string representation of the post, useful for debugging.
    """
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True
        )
    body: so.Mapped[str] = so.mapped_column(
        sa.String(140)
        )
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True,
        default=lambda: datetime.now(timezone.utc)
        )
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.id),
        index=True
        )
    author: so.Mapped[User] = so.relationship(
        back_populates='posts'
        )

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Querying the DB for specific values using .select and .where
# >>> query = sa.select(User).where(User.username.like('s%'))
# >>> db.session.scalars(query).all()
