from easyaccomod.room_models import Comment, Like
from os import urandom
from easyaccomod.owner_models import Owner, Room, City, District, Ward
from easyaccomod import db, bcrypt
import hashlib
import re
from easyaccomod.models import User, Post
from easyaccomod.admin.utils import save_room_picture

def encrypt_string(hash_string):
	bcrypt_hash = bcrypt.generate_password_hash(hash_string).decode('utf-8')
	return bcrypt_hash

def genrate_random_string(length):
    return urandom(length//2).hex()


def add_user(username, password, check_password, email, fullname, identity_number, phone_number, city_code, district_id, ward_id, commit=True):
	regex_user = '^[a-zA-Z0-9]+([a-zA-Z0-9](_|-| )[a-zA-Z0-9])*[a-zA-Z0-9]+$'
	if not re.search(regex_user, username):
		return (False, 'Tên đăng nhập không hợp lệ')
	user = db.session.query(User).filter_by(username=username).first()
	if user:
		return (False, 'Người dùng đã tồn tại')

	if len(password) < 6:
		return (False, 'Mật khẩu quá ngắn')
	if password != check_password:
		return (False, 'Mật khẩu nhập lại không trùng khớp')
	
	regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if not re.search(regex_email, email):
		return (False, 'Email không hợp lệ')
	check_mail = db.session.query(User).filter_by(email = email).first()
	if check_mail:
		return (False, 'Email đã được sử dụng')

	if not phone_number.isnumeric():
		return (False, 'Số điện thoại không hợp lệ')
	check_phone_number = db.session.query(Owner).filter_by(phone_number = phone_number).first()
	if check_phone_number:
		return (False, 'Số điện thoại đã được sử dụng')
	
	if not identity_number.isnumeric():
		return (False, 'Số CCCD/CMND không hợp lệ')
	check_address = db.session.query(Ward).filter_by(city_code = city_code, district_id = district_id, id = ward_id).first()
	if not check_address:
		return (False, 'Địa chỉ không hợp lệ')

	hashed = encrypt_string(password)
	new_user = User(username=username, password=hashed, email=email, role_id=3, status_confirm=2)
	db.session.add(new_user)
	db.session.flush()
	new_owner = Owner(username=username,
					password=hashed,
					fullname=fullname,
					phone_number=phone_number,
					identity_number=identity_number,
					email=email,
					city_code=city_code,
					district_id=district_id,
					ward_id=ward_id,
					user_id=new_user.id
					)
	db.session.add(new_owner)
	if(commit):
		db.session.commit()

	return (True, 'Đăng kí thành công')

def check_user(username, password):
	user = db.session.query(User).filter_by(username=username).first()

	if not user:
		return (False, "Không tồn tại tài khoản.")
	if user.status_confirm == 2:
		return (False, "Tài khoản chưa được xác thực, vui lòng đợi.")
	if user.status_confirm == 3:
		return (False, "Tài khoản đang bị khóa, vui lòng liên hệ với công ty để được giải quyết.")
	if bcrypt.check_password_hash(user.password, password):
		return (True, user)
	else:
		return (False, "Thông tin đăng nhập không chính xác.")


def change_password(username, password, newpassword, renewpassword):
	if(len(newpassword) < 6):
		return (False, "Mat khau qua ngan")
	if(newpassword != renewpassword):
		return (False, "Mat khau nhap lai khong trung khop")
	user = User.query.filter_by(username = username).first()
	if(not bcrypt.check_password_hash(user.password, password)):
		return (False, "Mat khau hien tai khong dung")
	if(bcrypt.check_password_hash(user.password, newpassword)):
		return (False, "Mat khau moi phai khac mat khau hien tai")
	user.password = encrypt_string(newpassword)
	db.session.commit()
	return (True, "Doi mat khau thanh cong")

def add_city(code, name, commit=True):
	new_city = City(code=code, name=name)
	db.session.add(new_city)
	if commit:
		db.session.commit()

def add_district(city_code,id, name, commit=True):
	new_district = District(city_code=city_code, id=id, name=name)
	db.session.add(new_district)
	if commit:
		db.session.commit()

def add_ward(city_code, district_id, id, name, commit=True):
	new_ward = Ward(city_code=city_code, district_id=district_id, id=id, name=name)
	db.session.add(new_ward)
	if commit:
		db.session.commit()

def add_room(user_id, room, image, commit = True):
	print(room)
	room_attrs = ["dien_tich", "loai_phong_tam", "loai_phong_bep", "info", "room_type_id", "room_number", "price", "phong_tam", "phong_bep", "gia_dien", "gia_nuoc", "chung_chu", "nong_lanh", "dieu_hoa", "ban_cong", "tien_ich_khac"]
	new_room = Room()
	new_room.status = False
	setattr(new_room, "user_id", user_id)
	setattr(new_room, "city_code", room["city"])
	setattr(new_room, "district_id", room["district"])
	setattr(new_room, "ward_id", room["ward"])
	for attr in room_attrs:
		setattr(new_room, attr, room[attr])
	try:
		db.session.add(new_room)
		db.session.flush()
	except:
		return ("error", "co loi xay ra, vui long thu lai")
	img = []
	for i in image:
		filename = save_room_picture(str(new_room.id), i)
		img.append(filename)
	new_room.image = str(img)
	new_post = Post()
	setattr(new_post, "title", room["title"])
	setattr(new_post, "content", room["info"])
	setattr(new_post, "room_id", new_room.id)
	setattr(new_post, "user_id", user_id)
	setattr(new_post, "pending", False)
	db.session.add(new_post)
	db.session.flush()
	if commit:
		db.session.commit()
	return ("success", f"them thanh cong room_id={new_room.id}, post_id={new_post.id}")

def get_room(id, user_id):
	try:
		room = Room.query.filter_by(id=id).first()
		if(room == None):
			return ("error", "khong ton tai phong")
		if(room.user_id != user_id):
			return ("error", "Permission Denied")
		return ("success", room)
	except:
		return ("error", "co loi xay ra")


def get_rooms(user_id):
	rooms = Room.query.filter_by(user_id=user_id)
	return rooms

def get_posts(user_id):
	posts = Post.query.filter_by(user_id=user_id)
	return posts


def get_post(id, user_id):
	try:
		post = Post.query.filter_by(id=id).first()
		if(post == None):
			return ("error", "khong ton tai bai dang")
		if(post.user_id != user_id):
			return ("error", "Permission Denied")
		return ("success", post)
	except:
		return ("error", "co loi xay ra")

def update_post(post, form):
	room_attrs = ["info", "dien_tich" ,"room_type_id", "room_number", "price", "phong_tam", "loai_phong_tam" ,"phong_bep", "loai_phong_bep","gia_dien", "gia_nuoc", "chung_chu", "nong_lanh", "dieu_hoa", "ban_cong", "tien_ich_khac"]
	new_post = post
	post.title = form["title"]
	post.content = form["info"]
	new_room = post.room
	for attr in room_attrs:
		setattr(new_room, attr, form[attr])
	try:
		db.session.add(new_room)
		db.session.add(new_post)
		db.session.flush()
	except:
		return ("error", "co loi xay ra, vui long thu lai")
	db.session.commit()
	return ("success", f"sua thanh cong id={new_post.id}")

def delete_post(post_id, user_id):
	# try:
	post = Post.query.filter_by(id=post_id).first()
	if(post == None):
		return ("error", "khong ton tai bai dang")
	if(post.user_id != user_id):
		return ("error", "Permission Denied")
	Comment.query.filter_by(post_id=post_id).delete()
	Like.query.filter_by(post_id=post_id).delete()
	db.session.delete(post)
	db.session.commit()
	return ("success", f"xoa thanh cong bai post_id={post.id}")
	# except:
	# 	return ("error", "co loi xay ra")

def update_status(post_id, user_id):
	post = Post.query.filter_by(id=post_id).first()
	if(post == None):
		return ("error", "khong ton tai bai dang", "")
	if(post.user_id != user_id):
		return ("error", "Permission Denied", "")
	if(post.room.status == False):
		post.room.status = True
		db.session.commit()
		return ("success", "thanh cong", 'Chuyển trạng thái thành "Chưa cho thuê"')
	else:
		post.room.status = False
		db.session.commit()
		return ("success", "thanh cong", 'Chuyển trạng thái thành "Đã cho thuê"')

def get_owner_by_username(username):
	owner = Owner.query.filter_by(username=username).first()
	if(owner == None):
		return ("error", "Khong ton tai")
	return ("success", owner)