from easyaccomod import db, app, login_manager
from easyaccomod.models import *
from easyaccomod.owner_models import Room

class Like(db.Model):
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


class Comment(db.Model):
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    comment_content = db.Column(db.Text, nullable = False)
    status = db.Column(db.Boolean)