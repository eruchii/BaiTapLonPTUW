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
	user = db.session.query(User).filter_by(username=username).first()
	if user:
		return (False, 'Người dùng đã tồn tại')

	if len(password) < 6:
		return (False, 'Mật khẩu quá ngắn')
	if password != check_password:
		return (False, 'Mật khẩu nhập lại không trùng khớp')
	
	regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if not re.search(regex, email):
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
	check_identity_number = db.session.query(Owner).filter_by(identity_number = identity_number).first()
	if check_identity_number:
		return (False, 'Số CCCD/CMND đã được sử dụng')
	
	check_address = db.session.query(Ward).filter_by(city_code = city_code, district_id = district_id, id = ward_id).first()
	if not check_address:
		return (False, 'Địa chỉ không hợp lệ')

	hashed = encrypt_string(password)
	new_user = User(username=username, password=hashed, email=email, role_id=2, status_confirm=0)
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
					user_id=new_user.id,
					status=0
					)
	db.session.add(new_owner)
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
	
def add_room(owner_id, city_code, district_id, ward_id, info, room_type_id, room_number, 
			price, chung_chu, phong_tam, nong_lanh, phong_bep, dieu_hoa, ban_cong, gia_dien, 
			gia_nuoc, tien_ich_khac, image, pending, commit=True):
	check_address = db.session.query(Ward).filter_by(city_code = city_code, district_id = district_id, id = ward_id).first()
	if not check_address:
		return (False, 'Địa chỉ không hợp lệ')

	try:
		new_room = Room(owner_id, city_code, district_id, ward_id, info, room_type_id, room_number, 
						int(price), int(chung_chu), int(phong_tam), int(nong_lanh), int(phong_bep), int(dieu_hoa), int(ban_cong), 
						int(gia_dien), int(gia_nuoc), tien_ich_khac, image, pending)
		db.session.add(new_room)
		if commit:
			db.session.commit()
		return (True, new_room.id)
	except:
		return (False, 'Có lỗi xảy ra, vui lòng kiểm tra lại thông tin')