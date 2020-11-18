from os import urandom
from easyaccomod.owner_models import Owner, Room, City, District, Ward
from easyaccomod import db, bcrypt
import hashlib
import re
from easyaccomod.models import User

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
		return (False, None)
	if user.status_confirm == 2:
		return (False, "Tài khoản chưa được xác thực, vui lòng đợi.")
	if user.status_confirm == 3:
		return (False, "Tài khoản đang bị khóa, vui lòng liên hệ với công ty để được giải quyết.")
	if bcrypt.check_password_hash(user.password, password):
		return (True, user)
	else:
		return (False, None)


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
