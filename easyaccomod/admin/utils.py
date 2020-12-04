from easyaccomod.chat import send_new_notification
from easyaccomod.room_models import Comment
import itertools
import random
from operator import pos
import os, secrets
from PIL import Image
from flask import url_for, current_app
from easyaccomod.owner_models import Room
from datetime import datetime
from easyaccomod import bcrypt, db
from easyaccomod.models import Notification, Post, User
from easyaccomod.owner_models import *


def addUserByAdmin(username, password, email):
    """
    function: add user by admin -> status_confirm = 1 : OK
    user is added to the user table immediately with status "OK"
    should be used : force add owner by admin to table user
    """
    tmpUser = User.query.filter_by(username=username).first()
    tmpUser2 = User.query.filter_by(email=email).first()
    if tmpUser or tmpUser2:
        print("Exist User")
        return False
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        owner = User(
            username=username,
            email=email,
            password=hashed_password,
            role_id=3,
            status_confirm=1,
        )
        db.session.add(owner)
        db.session.commit()
        return owner.id


def addUserByOwner(username, password, email):
    """
    function:: add user by owner : -> add a owner to table user, but status = WAIT
    para password : should be plaintext
    para email: unique same owner.email
    ---- return id of user added ----
    """
    tmpUser = User.query.filter_by(username=username).first()
    tmpUser2 = User.query.filter_by(email=email).first()
    if tmpUser or tmpUser2:
        print("Exist User")
        return False
    else:
        hash_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        owner = User(
            username=username,
            email=email,
            password=hash_pw,
            role_id=3,
            status_confirm=2,
        )
        db.session.add(owner)
        db.session.commit()
        return owner.id


def createPostByAdmin(title, content, room_id, date_out, admin_id):
    """
    function should be used by admin. pls check role_id before use it
    post created by admin// auto pending = True : da dc xu ly xong r
    para :: admin_id => call by admin and get 'current_id' of admin
    """
    post = Post(
        title=title, content=content, room_id=room_id, pending=True, date_out=date_out, user_id=admin_id
    )  # pending = True -> xly xong r
    post.date_posted = datetime.utcnow()
    db.session.add(post)
    db.session.commit()


def deletePostByID(post_id):
    """
    function: delete post, should be used by admin
    pls check role_id before used it
    """
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()


def checkUserExist(user_id):
    """
    check: user does exist in table user
    True -> exist
    False -> not exist
    """
    user = User.query.filter_by(id=user_id).first()
    if user:
        return True
    else:
        return False


def checkRoomExist(room_id):
    """
    check: room does exist in table room
    True -> exist : get room_id to post
    False -> not exist: can't create post with room_id
    """
    room = Room.query.filter_by(id=room_id).first()
    if room:
        return True
    else:
        return False


def acceptOwner(user_id):
    """
    accept owner by admin
    should be used for admin : accept account of owner
    change status_confirm to OK
    """
    user_accept = User.query.get_or_404(user_id)
    user_accept.status_confirm = 1
    db.session.commit()


def rejectUser(user_id):
    """
    reject owner by admin
    should be used for admin : reject account of owner
    change status_confirm to REJECT
    can use to ban owner ??
    """
    user_reject = User.query.filter_by(id=user_id).first()
    if user_reject:
        user_reject.status_confirm = 3
        db.session.commit()
        return user_reject.id
    else:
        return -1

def findUser(user_name):
    req_str = "%" + user_name + "%"
    print(req_str)
    user = User.query.filter(User.username.like(req_str)).all()
    return user

def sendNotification(receiver, title, msg):
    notification = Notification(receiver=receiver, title=title, msg=msg)
    db.session.add(notification)
    db.session.commit()
    data = {"id":notification.id}
    send_new_notification(data)
    print(notification)

def save_user_picture(user_prefix, form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = user_prefix + "_" + random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )
    i = Image.open(form_picture)
    width, height = i.size
    output_size = (width, height)
    if width > 160 or height > 160:
        if width > height :
            width = 160
            height = height/width * 160
        else :
            height = 160
            width = width/height * 160
        output_size = (width, height)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_room_picture(room_id, room_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(room_picture.filename)
    picture_fn = "room" + room_id + "_" + random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/room_pics", picture_fn
    )
    i = Image.open(room_picture)
    width, height = i.size
    output_size = (width, height)
    if width > 800 or height > 800:
        if width > height :
            width = 800
            height = height/width * 800
        else :
            height = 800
            width = width/height * 800
        output_size = (width, height)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def get_data_post_in_a_year(year):
    year = int(year)
    ans = []
    posts = Post.query.filter(Post.date_created >= datetime(year=year,month=1,day=1), Post.date_created < datetime(year=year+1,month=1,day=1)).all()
    for i in range(1,13):
        count = 0
        for post in posts:
            if post.date_created.month == i:
                count += 1
        ans.append(count)
    return ans

def get_data_user_register_in_a_year(year):
    year = int(year)
    ans = []
    users = User.query.filter(User.date_created >= datetime(year=year,month=1,day=1), User.date_created < datetime(year=year+1,month=1,day=1)).all()
    for i in range(1,13):
        count = 0
        for user in users:
            if user.date_created.month == i:
                count += 1
        ans.append(count)
    return ans

def statistic_cost_room():
    """
    return: 1 list chua so luong cac phong trong he thong theo thang gia 1 trieu dong
    """
    ans = []
    rooms = Room.query.all()
    max_room_cost = 0
    for room in rooms:
        if room.price > max_room_cost:
            max_room_cost = room.price
    # sdung thang do 1 trieu dong =()=
    length = int(max_room_cost / 1000000)
    for i in range(0, length+1):
        ans.append(0)
    for room in rooms:
        req = int(room.price / 1000000)
        ans[req] += 1
    return ans

def most_city_room(limit: int):
    """
    return: 2 list cac tinh co nhieu room nhat trong he thong va so luong room cua moi tinh do
    """
    limit = int(limit)
    ans = []
    city = City.query.all()
    rooms = Room.query.all()
    req = {}
    for c in city:
        req[c.name] = 0
    for room in rooms:
        req[room.city.name] += 1
    req = dict(sorted(req.items(), key=lambda item: item[1], reverse=True))
    req = dict(itertools.islice(req.items(), limit))
    ans.append(list(req.keys()))
    ans.append(list(req.values()))
    return ans

















################ FAKE UTILS ##################
def fake_add_user():
    for i in range(1,100):
        usn = "fakeuser" + str(i)
        email = "fakeuser" + str(i) + ".fake@gmail.com"
        pw = "123456"
        addUserByAdmin(usn,pw,email)

def fake_add_renter():
    for i in range(1,50):
        usn = "fakerenter" + str(i)
        email = "fakerenter" + str(i) + ".fake@gmail.com"
        pw = "123456"
        tmpUser = User.query.filter_by(username=usn).first()
        tmpUser2 = User.query.filter_by(email=email).first()
        if tmpUser or tmpUser2:
            print("Exist User")
            return False
        else:
            hashed_password = bcrypt.generate_password_hash(pw).decode("utf-8")
            renter = User(
                username=usn,
                email=email,
                password=hashed_password,
                role_id=2,
                status_confirm=1,
            )
            db.session.add(renter)
            db.session.commit()

def fake_add_comment():
    for i in range(1,50):
        comment = Comment(post_id=random.randint(1,4), user_id=(i+60), comment_content=f"comment content {i}", status=False)
        db.session.add(comment)
    db.session.commit()