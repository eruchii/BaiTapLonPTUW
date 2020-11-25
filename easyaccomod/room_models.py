from easyaccomod import db, app, login_manager
from easyaccomod.models import *
from easyaccomod.owner_models import Room

class Like(db.Model):
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable = False,unique= False,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False,unique = False,primary_key=True)
    def __repr__(self):
        return (f"Like for '{self.room_id}' from '{self.user_id}'")
        
class Comment(db.Model):
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'),nullable = False,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False,primary_key=True)
    comment_content = db.Column(db.Text, nullable = False,primary_key=True)
    status = db.Column(db.Boolean,nullable = False)
    def __repr__(self):
        return (f"Comment : '{self.comment_content}' for '{self.room_id}' by user '{self.user_id}''")