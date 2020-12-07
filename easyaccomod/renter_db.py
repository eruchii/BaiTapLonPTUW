from easyaccomod.owner_models import Owner, Room, City, District, Ward
from easyaccomod import db, bcrypt
from easyaccomod.models import User
from easyaccomod.room_models import *

def addLike(user_id,room_id,commit=True):
    existCheck = db.session.query(Like).\
        filter_by(user_id = user_id).\
          filter_by(room_id = room_id).first()
    if existCheck != None:
        return (False,"Already liked")
    else :
        new_like = Like(user_id = user_id, room_id = room_id)
        db.session.add(new_like)
    if (commit):
        db.session.commit()
    return (True,f"Successfully liked for {user_id} of room number {room_id}")

def removeLike(user_id,room_id,commit=True):
    existCheck = db.session.query(Like).\
        filter_by(user_id = user_id).\
          filter_by(room_id = room_id).first()
    if existCheck != None:
        db.session.delete(existCheck)
    else:
        return (False,"Already Unliked")
    if (commit):
        db.session.commit()
    return (True,f"Successfully Unliked for {user_id} of room number {room_id}")

def addComment(user_id,room_id,content,commit = True):
    existCheck = db.session.query(Comment).\
        filter_by(user_id = user_id).\
          filter_by(room_id = room_id).\
              filter_by(comment_content = content).first()
    if existCheck != None:
        return (False,"Already Commented this comment")
    else :
        cmt = Comment(user_id = user_id,room_id = room_id,comment_content = content,status = False)
        db.session.add(cmt)
    if (commit):
        db.session.commit()
    return (True,"Comment Succesfully Created!")

def addPriceLog(price):
    priceRange = PriceLog(price)
    db.session.add(priceRange)
    db.session.commint()