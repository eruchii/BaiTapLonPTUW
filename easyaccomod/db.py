from os import urandom
from easyaccomod.owner_models import Owner, Room, City, District, Ward
from easyaccomod import db
import hashlib
import re

def encrypt_string(hash_string):
	sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
	return sha_signature

def genrate_random_string(length):
    return urandom(length//2).hex()


def add_user(username, password, check_password, email, fullname, identity_number, phone_number, city_code, district_id, ward_id, commit=True):
	user = db.session.query(Owner).filter_by(username=username).first()
	if user:
		return (False, 'Người dùng đã tồn tại')

	if len(password) < 6:
		return (False, 'Mật khẩu quá ngắn')
	if password != check_password:
		return (False, 'Mật khẩu nhập lại không trùng khớp')
	
	regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if not re.search(regex, email):
		return (False, 'Email không hợp lệ')
	check_mail = db.session.query(Owner).filter_by(email = email).first()
	if check_mail:
		return (False, 'Email đã được sử dụng')

	if not phone_number.isnumeric():
		return (False, 'Số điện thoại không hợp lệ')
	check_phone_number = db.session.query(Owner).filter_by(phone_number = phone_number).first()
	if check_phone_number:
		return (False, 'Số điện thoại đã được sử dụng')
	
	if not identity_number.isnumeric():
		return (False, 'Số CCCD/CMND không hợp lệ')
	check_identity_number = db.session.query(Owner).filter_by(identity_number = identity_number).first()
	if check_identity_number:
		return (False, 'Số CCCD/CMND đã được sử dụng')
	
	check_address = db.session.query(Ward).filter_by(city_code = city_code, district_id = district_id, id = ward_id).first()
	if not check_address:
		return (False, 'Địa chỉ không hợp lệ')

	hashed = encrypt_string(password)
	
	new_user = Owner(username=username,
					password=hashed,
					fullname=fullname,
					phone_number=phone_number,
					identity_number=identity_number,
					email=email,
					city_code=city_code,
					district_id=district_id,
					ward_id=ward_id,
					status=0
					)
	db.session.add(new_user)
	if(commit):
		db.session.commit()

	return (True, 'Đăng kí thành công')


def user_exists(username):
	user = db.session.query(Owner).filter_by(username=username).first()

	if not user:
		return (False, 'Người dùng không tồn tại')

	return (True, 'Người dùng tồn tại')


def check_user(username, password):
	user = db.session.query(Owner).filter_by(username=username).first()

	if not user:
		return (False, 'Không thành công')

	if encrypt_string(password) == user.password:
		return (True, "Thành công")
	else:
		return (False, 'Không thành công')

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
	
def add_room(owner_id, city_code, district_id, ward_id, info, room_type_id, room_number, price, chung_chu, phong_tam, nong_lanh, phong_bep, dieu_hoa, ban_cong, gia_dien, gia_nuoc, tien_ich_khac, image, pending, commit=True):
	check_address = db.session.query(Ward).filter_by(city_code = city_code, district_id = district_id, id = ward_id).first()
	if not check_address:
		return (False, 'Địa chỉ không hợp lệ')

	new_room = Room(owner_id, city_code, district_id, ward_id, info, room_type_id, room_number, price, chung_chu, phong_tam, nong_lanh, phong_bep, dieu_hoa, ban_cong, gia_dien, gia_nuoc, tien_ich_khac, image, pending)
	db.session.add(new_room)
	return (True, 'Gửi bài đăng cho admin duyệt thành công!')
	if commit:
		db.session.commit()