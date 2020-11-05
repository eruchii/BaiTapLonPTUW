from __init__ import db, app, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    name = db.Column(db.String(30), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    users = db.relationship('User', backref="roles", lazy=True)
    def __repr__(self):
        return f"Role('{self.id}', '{self.title}', '{self.name}')"

class Confirm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    users = db.relationship('User', backref="confirms", lazy=True)
    def __repr__(self):
        return f"Confirm('{self.id}', '{self.name}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    status_confirm = db.Column(db.Integer, db.ForeignKey('confirm.id'), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}, '{self.image_file}')"
    
