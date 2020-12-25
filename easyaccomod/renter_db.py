from easyaccomod.owner_models import Owner, Room, City, District, Ward
from easyaccomod import db, bcrypt
from easyaccomod.models import User,Post
from easyaccomod.room_models import *

def addLike(user_id,post_id,commit=True):

    existCheck = db.session.query(Like)\
        .filter_by(user_id = user_id)\
          .filter_by(post_id = post_id).first()

    if existCheck != None:
        return (False,"Already liked")
    else :
        new_like = Like(user_id = user_id, post_id = post_id)
        db.session.add(new_like)
    if (commit):
        db.session.commit()
    return (True,f"Successfully liked for {user_id} of post number {post_id}")

def removeLike(user_id,post_id,commit=True):
    existCheck = db.session.query(Like)\
        .filter_by(user_id = user_id)\
          .filter_by(post_id = post_id).first()
    if existCheck != None:
        db.session.delete(existCheck)
    else:
        return (False,"Already Unliked")
    if (commit):
        db.session.commit()
    return (True,f"Successfully Unliked for {user_id} of post number {post_id}")

def addComment(user_id,post_id,content,commit = True):

    existCheck = db.session.query(Comment)\
        .filter_by(user_id = user_id)\
          .filter_by(post_id = post_id)\
              .filter_by(comment_content = content).first()

    if existCheck != None:
        return (False,"Already Commented this comment")
    else :
        cmt = Comment(user_id = user_id,post_id = post_id,comment_content = content,status = False)
        db.session.add(cmt)
    if (commit):
        db.session.commit()
    return (True,"Comment Succesfully Created!")

def addPriceLog(price):
    priceRange = PriceLog(price)
    db.session.add(priceRange)
    db.session.commit()


def defaultSearch(city,district,street):
    city_code = db.session.query(City).filter_by(name = city).first().code
    district_code = db.session.query(District).filter_by(name=district).first().id
    street_code = db.session.query(Ward).filter_by(name=street).first().id
    res = []
    res = db.session.query(Room).\
        filter_by(city_code = city_code).\
            filter_by(district_code = district_code).\
                filter_by(ward_id= street_code)
    if res == []:
        return "Can't Find Your Perfect Home"
    return res


def getRoomById(room_id):
    try:
        room = db.session.query(Room).filter_by(id = room_id).filter(Room.post.any()).first()
        if room == None:
            return ("error", "khong ton tai phong")
        else:
            return ("success", room)
    except:
        return ('error','co loi xay ra')

def getPostByRoomID(room_id):
    try:
        post = Post.query.filter_by(room_id = room_id).order_by(Post.date_out.desc()).first()
        if post == None:
            return ("error", "khong ton tai phong")
        else:
            return ("success",post)
    except:
        return ('error','co loi xay ra')

def checkLikeByUser(user_id,post_id):
    try:
        liked = Like.query.filter_by(user_id = user_id).filter_by(post_id=post_id).first()
        if liked is None:
            return ("False")
        else: 
            return ("True")
    except:
        return ('error','co loi xay ra')