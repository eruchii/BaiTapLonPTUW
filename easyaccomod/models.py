from sqlalchemy.orm import backref
from easyaccomod import db, app, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from easyaccomod.owner_models import *

# callback -> This callback is used to reload the user object from the user ID stored in the session
# It should take the unicode ID of a user, and return the corresponding user object.
# It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

time_delay = timedelta(days=7)  # default: delay post 7days for processing post
time_out = timedelta(weeks=4)   # default: a post can be published in 4 weeks from the time of submission

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    name = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    users = db.relationship("User", backref="roles", lazy=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.title}', '{self.name}')"


class Confirm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    users = db.relationship("User", backref="confirms", lazy=True)

    def __repr__(self):
        return f"Confirm('{self.id}', '{self.name}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default="default.jpg")
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    status_confirm = db.Column(db.Integer, db.ForeignKey("confirm.id"), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    owner = db.relationship('Owner', backref='users', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}, '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    pending = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    date_posted = db.Column(db.DateTime, nullable=False, default=(datetime.utcnow() + time_delay))
    date_out = db.Column(db.DateTime, nullable=False, default=(datetime.utcnow() + time_out))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # fix:: author !important

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # receiver
    shortdescription = db.Column(db.String(150), nullable=False)
    msg = db.Column(db.Text, nullable=False)
    count_notification = db.Column(db.Integer, nullable=False, default=0)
    seen_notification = db.Column(db.Boolean, nullable=False, default=True)  # True -> da xem, False -> chua xem
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Notification('{self.id}', '{self.receiver}', '{self.msg}')"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), db.ForeignKey('user.username'), nullable=False) # sender
    receiver = db.Column(db.String(120), db.ForeignKey('user.username'), nullable=False) # receiver
    content = db.Column(db.String(120))
    seen = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Message('{self.id}', '{self.sender}', '{self.receiver}','{self.content}')"
