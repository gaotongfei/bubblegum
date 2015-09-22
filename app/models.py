from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    website = db.Column(db.String(50))
    bio = db.Column(db.String(200))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        return 'https://gravatar.com/avatar/%s?d=retro&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    permission = db.Column(db.Integer, default=0)

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(2000))
    body_md = db.Column(db.String(3000))
    node = db.Column(db.String(20))
    username = db.Column(db.String(20))
    post_time = db.Column(db.DateTime, default=datetime.utcnow)
    latest_update_time = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(200))


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    comment_time = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(20))
    avatar = db.Column(db.String(200))


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    from_post_id = db.Column(db.Integer)
    from_post_title = db.Column(db.String(100))
    is_read = db.Column(db.Integer, default=0)
    from_id = db.Column(db.String(20))
    to_id = db.Column(db.String(20))
    message = db.Column(db.String(500))
    message_time = db.Column(db.DateTime, default=datetime.utcnow)


class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    node = db.Column(db.String(20), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '%r' % self.node


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
