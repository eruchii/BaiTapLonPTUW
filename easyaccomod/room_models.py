from datetime import datetime, timedelta
from easyaccomod import db, app, login_manager
from easyaccomod.models import *
# from easyaccomod.owner_models import Room

class Like(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable = False,unique= False,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False,unique = False,primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship("Post", backref="like", lazy=True)
    def __repr__(self):
        return (f"Like for '{self.post_id}' from '{self.user_id}'")
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    comment_content = db.Column(db.Text, nullable = False)
    status = db.Column(db.Boolean,nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return (f"Comment : '{self.comment_content}' for '{self.post_id}' by user '{self.user_id}''")

class PriceLog(db.Model):   
    id = db.Column(db.Integer,primary_key=True)
    priceRange = db.Column(db.String(30))
    count = db.Column(db.Integer, nullable=False, default=0)
    def __repr__(self):
        return (f"Price Range : '{self.id}' - '{self.priceRange}'")