from app import db

from typing import Optional
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from hashlib import md5



class User(UserMixin, db.Model):
    """
    An SQLAlchemy model representing a user in the system.

    Attributes:
        id (int): Unique primary key for each user.
        username (str): A unique username (max 64 characters).
        email (str): A unique email address (max 120 characters).
        password_hash (str, optional): The hashed password (max 256 characters).
        posts (List[Post]): A one-to-many relationship to posts authored by the user.
        about_me (str, optional): A brief user bio (max 140 characters).
        last_seen (datetime, optional): The last time the user was seen (defaults to current UTC time).
        followers (Table): Association table for self-referential many-to-many relationship to track followers.
        followers: Association table for self-referential many-to-many relationship to track followers.
        following: Association table for self-referential many-to-many relationship to track followed users.

    Methods:
        __repr__(): Returns a readable string representation of the user (e.g., <User johndoe>).
        set_password(password): Hashes and stores the provided password.
        check_password(password): Verifies a provided password against the stored hash.
        load_user(id): Returns the user with the id specified.
        avatar(size): Return the users gravatar icon.
        follow(user): Follow a user.
        unfollow(user): Unfollow a user.
        is_following(user): Check if the current user is following another user.
        followers_count(): Returns the number of followers the user has.
        following_count(): Returns the number of users the user is following.
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

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    followers = sa.Table(
        'followers',
        db.metadata,
        sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
                  primary_key=True),
        sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
                  primary_key=True)
    )

    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None
    
    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)

    def following_posts(self):
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(sa.or_(
                Follower.id == self.id,
                Author.id == self.id,
            ))
            .group_by(Post)
            .order_by(Post.timestamp.desc())
        )
    
    # @login.user_loader
    # def load_user(id):
    #     return db.session.get(User,int(id))


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