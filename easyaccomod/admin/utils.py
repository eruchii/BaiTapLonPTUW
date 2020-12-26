from easyaccomod.chat import send_new_notification
from easyaccomod.room_models import *
import itertools
import random
import os, secrets
from PIL import Image
from flask import url_for, current_app
from easyaccomod.owner_models import Room
from datetime import datetime
from easyaccomod import bcrypt, db, celery
from easyaccomod.models import Notification, Post, User
from easyaccomod.owner_models import *
from easyaccomod import mail, Message


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

def accept_comment(comment_id):
    """
    param: comment_id : id of comment to accept
    """
    comment_accept = Comment.query.get(comment_id)
    if comment_accept:
        comment_accept.status = True
        db.session.commit()
        return comment_accept.id
    else :
        return -1

def reject_comment(comment_id):
    """
    param: comment_id : id of comment to accept
    """
    comment_accept = Comment.query.get(comment_id)
    if comment_accept:
        comment_accept.status = False
        db.session.commit()
        return comment_accept.id
    else :
        return -1

def findUser(user_name, page, per_page):
    req_str = "%" + user_name + "%"
    user = User.query.filter(User.username.like(req_str)).order_by(User.id.asc()).paginate(page=page, per_page=per_page)
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

def statistic_price_log():
    ans = []
    price_logs = PriceLog.query.all()
    ans_name = []
    ans_count = []
    ans_data = {}
    for price_log in price_logs:
        ans_name.append(price_log.priceRange)
        ans_count.append(price_log.count)
        ans_data[price_log.priceRange] = price_log.count
    ans.append(ans_name)
    ans.append(ans_count)
    ans.append(ans_data)
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

def cac_tinh_duoc_xem_nhieu_nhat(limit: int):
    """
    return list cac tinh co tong luot xem post nhieu nhat va so luong tuong ung
    """
    ans = []
    city = City.query.all()
    posts = Post.query.all()
    req = {}
    for c in city:
        req[c.name] = 0
    for post in posts:
        req[post.room.city.name] += post.count_view
    req = dict(sorted(req.items(), key=lambda item: item[1], reverse=True))
    req = dict(itertools.islice(req.items(), limit))
    ans.append(list(req.keys()))
    ans.append(list(req.values()))
    return ans

def cac_quan_duoc_xem_nhieu_nhat(tinh: str, limit: int):
    """
    :return: list cac quan thuoc 1 tinh::arg co nhieu view nhat
    :param tinh: str - name of province
    :param limit: int - number of records you want
    """
    ans = []
    temp = []
    req = {}
    city = City.query.filter_by(name=tinh).first()
    if not city:
        ans.append("False")
        return ans
    districts = District.query.filter(District.city_code==city.code).all()
    posts = Post.query.all()
    for post in posts:
        if post.room.city.name == tinh:
            temp.append(post)
    for d in districts:
        req[d.name] = 0
    for t in temp:
        req[t.room.district.name] += t.count_view
    req = dict(sorted(req.items(), key=lambda item: item[1], reverse=True))
    req = dict(itertools.islice(req.items(), limit))
    ans.append(list(req.keys()))
    ans.append(list(req.values()))
    return ans








@celery.task
def send_reset_email(data):
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[data['user_email']])
    msg.body = data['body']
    mail.send(msg)









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
    posts = Post.query.all()
    l = len(posts)
    for i in range(1,50):
        comment = Comment(post_id=random.randint(1,l), user_id=(i+60), comment_content=f"comment content {i}", status=False)
        db.session.add(comment)
    db.session.commit()

def add_price_log():
    for i in range(1,11):
        price_log = PriceLog(priceRange=str(i-1) + " triệu - " + str(i) + " triệu")
        print(price_log)
        print(type(price_log.priceRange))
        db.session.add(price_log)
    price_log1 = PriceLog(priceRange="Trên 10 triệu")
    db.session.add(price_log1)
    db.session.commit()

def fake_add_data_price_log():
    price_logs = PriceLog.query.all()
    for i in range(1,1000):
        j = random.randint(0,10)
        price_logs[j].count += 1
    db.session.commit()

def add_dummy_room():
    wards = Ward.query.all()
    owners = Owner.query.all()
    for j in range(1, 100):
        for i in range(1,9):
            random_ward = random.randint(0, len(wards)-1)
            random_owner = random.randint(0, len(owners)-1)
            random_roomtype = random.randint(1,4)
            random_price = random.randint(10,99) * 100000
            random_dien_tich = random.randint(18,85)
            random_loai_phong_tam = random.randint(1,2)
            random_loai_phong_bep = random.randint(1,3)
            room_dummy = Room(user_id=owners[random_owner].user_id, city_code=wards[random_ward].city_code, 
                district_id=wards[random_ward].district_id, ward_id=wards[random_ward].id, info=f"Create room info",
                room_type_id=random_roomtype, room_number=random.randint(2,6), price=random_price, dien_tich=random_dien_tich, chung_chu=random.randint(0,1), phong_tam=random.randint(1,3), loai_phong_tam=random_loai_phong_tam,
                nong_lanh=random.randint(0,1), phong_bep=random.randint(1,2), loai_phong_bep=random_loai_phong_bep, dieu_hoa=random.randint(0,1), ban_cong=random.randint(0,1), gia_dien=random.randint(2000,4500), gia_nuoc=random.randint(7000,25000),
                image=f"['bancong{i}.jpeg', 'bedroom{i}.jpeg', 'kitchen{i}.jpeg', 'livingroom{i}.jpeg']", status=0)
            db.session.add(room_dummy)
            db.session.commit()

def add_dummy_post():
    owners = Owner.query.all()
    rooms = Room.query.all()
    for i in range(1,500):
        random_room = random.randint(0, len(rooms)-1)
        random_user = random.randint(0, len(owners)-1)
        title = f"Đăng bài cho thuê nhà {random.randint(1,1000)}"
        content = f"""Nhà có 8 Phòng đã cho thuê hết 7 cơ hội cho người có Duyên
Còn duy nhất 1 phòng cho thuê nốt chỉ 2,8 tr/tháng ở Phố Hàng Mành-Hà Nội.
Phòng Đẹp, khép kín, rộng 22m2, đầy đủ giường tủ, chăn đệm mới tinh chỉ việc dọn về ở.
Còn phòng cuối cùng nên giảm giá cho những ai may mắn, kinh tế eo hẹp.
Giờ giấc thoải mái , không chung chủ, An ninh đảm bảo. {random.randint(1,1000)}"""
        room_id = rooms[random_room].id
        pending = True
        user_id = owners[random_user].user_id
        post = Post(title=title, content=content, room_id=room_id, pending=pending, user_id=user_id)
        db.session.add(post)
    db.session.commit()