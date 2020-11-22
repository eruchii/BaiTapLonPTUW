from easyaccomod.owner_models import Owner, Room, City, District, Ward
from easyaccomod import db, bcrypt
from easyaccomod.models import User
from easyaccomod.room_models import Like,Comment

def addLike(user_id,room_id):
    existCheck = db.session.query(Like).\
        filter_by(user_id = data["user_id"]).\
          filter_by(room_id = data["room_id"]).first()
    if existCheck != None:
        return (False,"Already liked")
    else :
        new_like = Like(user_id = user_id, room_id = room_id)
        db.session.add(new_like)
    if (commit):
        db.session.commit()
    return (True,f"Successfully liked for {user_id} of room number {room_id}")

def removeLike(user_id,room_id):
    existCheck = db.session.query(Like).\
        filter_by(user_id = data["user_id"]).\
          filter_by(room_id = data["room_id"]).first()
    if existCheck != None:
        return (False,"Already Unliked")
    else:
        db.session.delete(existCheck)
    if (commit):
        db.session.commit()
    return (True,f"Successfully Unliked for {user_id} of room number {room_id}")

