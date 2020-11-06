from os import urandom
from easyaccomod.owner_models import Owner, Room
from easyaccomod import db
import hashlib

def encrypt_string(hash_string):
	sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
	return sha_signature

def genrate_random_string(length):
    return urandom(length//2).hex()


def add_user(username, password, check_password, fullname, identity_number, phone_number):
	user = db.session.query(Owner).filter_by(username=username).first()
	if user:
		return (False, 'Người dùng đã tồn tại')

	if len(password) < 6:
		return (False, 'Mật khẩu quá ngắn')

	if password != check_password:
		return (False, 'Mật khẩu nhập lại không trùng khớp')
	
	check_phone_number = db.session.query(Owner).filter_by(phone_number = phone_number).first()
	if check_phone_number:
		return (False, 'Số điện thoại đã được sử dụng')
	
	check_identity_number = db.session.query(Owner).filter_by(identity_number = identity_number).first()
	if check_identity_number:
		return (False, 'Số CCCD / CMND đã được sử dụng')

	hashed = encrypt_string(password)
	
	new_user = Owner(username=username,
					password=hashed,
					fullname=fullname,
					phone_number=phone_number,
					identity_number=identity_number,
					status=0
					)
	db.session.add(new_user)
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
