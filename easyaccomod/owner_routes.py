from flask import *
from easyaccomod import app
from flask_login import login_user, current_user, logout_user
from easyaccomod.owner_models import Owner, Room, User
from functools import wraps
from easyaccomod.owner_db import *

owner_bp = Blueprint("owner", __name__, template_folder='templates/owner')

def is_owner(f):
	@wraps(f)
	def decorated_func(*args, **kwargs):
		if(current_user.is_anonymous):
			return redirect(url_for("owner.login"))
		if(current_user.role_id != 3):
			abort(403)
		return f(*args, **kwargs)
	return decorated_func

@owner_bp.route("/api/register", methods = ["POST"])
def api_register():
	res = {}
	res["status"] = "error"
	res["msg"] = "dang ky khong thanh cong"
	data = request.get_json()
	try:
		status, msg = add_user(data["username"], data["password"], 
								data["check_password"], 
								data["email"], 
								data["fullname"], 
								data["identity_number"], 
								data["phone_number"], 
								data["city_code"], 
								data["district_id"], 
								data["ward_id"])
		if status:
			res["status"] = "success"
		else:
			res["status"] = "fail"
		res["msg"] = msg
		return jsonify(res)
	except:
		return jsonify(res)


@owner_bp.route("/register")
def register():
	if(current_user.is_authenticated):
		return redirect(url_for("main.home"))
	return render_template("owner/register.html", title="Đăng ký")

@owner_bp.route("/api/login", methods=["POST"])
def api_login():
	res = {}
	res["status"] = "error"
	res["msg"] = "dang nhap khong thanh cong"
	data = request.get_json()
	try:
		username = data["username"]
		password = data["password"]
	except:
		return jsonify(res)
	
	status, resp = check_user(username=username, password=password)
	if status:
		res["status"] = "success"
		res["msg"] = "Đăng nhập thành công"
		login_user(resp, remember=True)
	else:
		res["msg"] = resp
	
	return jsonify(res)

@owner_bp.route("/login")
def login():
	if(current_user.is_authenticated):
		return redirect(url_for("main.home"))
	return render_template("owner/login.html", title="Đăng nhập")

@owner_bp.route("/changepassword")
@is_owner
def changepassword():
	return render_template("owner/changepassword.html", title="Đổi mật khẩu")

@owner_bp.route("/api/changepassword", methods=["POST"])
@is_owner
def api_change_password():
	res = {}
	res["status"] = "error"
	res["status"] = "doi mat khau khong thanh cong"
	data = request.get_json()
	try:
		password = data["password"]
		newpassword = data["newpassword"]
		renewpassword = data["renewpassword"]
	except:
		return jsonify(res)
	status, resp = change_password(current_user.username, password, newpassword, renewpassword)
	if status:
		res["status"] = "success"
		res["msg"] = "Doi mat khau thanh cong"
	else:
		res["msg"] = resp
	
	return jsonify(res)

@owner_bp.route("/fakelogin/<id>")
def fakelogin(id):
	user = User.query.filter_by(id=id).first()
	login_user(user, remember=True)
	return jsonify({"status":"ok"})

@owner_bp.route("/")
@is_owner
def home():
	return redirect(url_for("owner.route_list_room"))

@owner_bp.route("/notification/")
@is_owner
def notification():
	return render_template("owner/notification.html", title="Thông báo")

@owner_bp.route("/logout/")
@is_owner
def logout():
	logout_user()
	return redirect(url_for("owner.login"))

@owner_bp.route("/room/create/")
@is_owner
def create_new_room():
	return render_template("owner/createroom.html", title="Tạo bài đăng mới")

@owner_bp.route("/api/room/create", methods=["POST"])
@is_owner
def api_create_new_room():
	res = {}
	res["status"] = "error"
	res["msg"] = ""
	data_form = request.form
	img = request.files.getlist("image")
	room_data = {}
	form_attrs = ["title", "city", "district", "ward", "info", "dien_tich", "room_type_id", "room_number", "price", "phong_tam", "loai_phong_tam", "phong_bep", "loai_phong_bep","gia_dien", "gia_nuoc", "tien_ich_khac"]
	int_fields = ["room_type_id", "room_number", "price", "phong_tam", "phong_bep", "gia_dien", "gia_nuoc", "dien_tich", "loai_phong_tam", "loai_phong_bep"]
	form_checkbox = ["chung_chu", "nong_lanh", "dieu_hoa", "ban_cong"]
	for attr in form_attrs:
		try:
			room_data[attr] = data_form[attr]
			if(room_data[attr] == ""):
				res["msg"] = "Thieu truong can thiet"
				return jsonify(res)
		except:
			res["msg"] = "Thieu truong can thiet"
			return jsonify(res)
	for f in int_fields:
		try:
			room_data[f] = int(room_data[f])
		except:
			res["msg"] = "Thong tin khong hop le"
			return jsonify(res)

	for attr in form_checkbox:
		try:
			x = data_form[attr]
			if(x == "on"):
				room_data[attr] = True
			else:
				room_data[attr] = False
		except:
			room_data[attr] = False
	if(len(img) < 3):
		res["msg"] = "Toi thieu 3 anh"
		return jsonify(res)
	status, msg = add_room(current_user.id, room_data, img)
	res["status"] = status
	res["msg"] = msg
	return jsonify(res)

@owner_bp.route("/api/room/get/<int:id>")
@is_owner
def api_get_room(id):
	res = {}
	res["status"] = "error"
	res["msg"] = "co loi xay ra"
	res["data"] = {}
	status, resp = get_room(id, current_user.id)
	if(status == "error"):
		res["status"] = status
		res["msg"] = resp
		return jsonify(res)
	attrs = ["info", "room_type_id", "room_number", "price", "phong_tam", "phong_bep", "gia_dien", "gia_nuoc", "chung_chu", "nong_lanh", "dieu_hoa", "ban_cong", "tien_ich_khac"]
	res["data"]["city"] = resp.city_code
	res["data"]["district"] = resp.ward_id
	res["data"]["ward"] = resp.ward_id
	for attr in attrs:
		res["data"][attr] = getattr(resp, attr)
	res["status"] = "success"
	res["msg"] = "thanh cong"
	return jsonify(res)

@owner_bp.route("/api/post/update/<int:id>", methods=["POST"])
@is_owner
def api_update_post(id):
	res = {}
	res["status"] = "error"
	res["msg"] = "co loi xay ra"
	status, resp = get_post(id, current_user.id)
	if(status == "error"):
		res["status"] = status
		res["msg"] = resp
		return jsonify(res)
	data_form = request.form
	room_data = {}
	form_attrs = ["title", "info", "dien_tich", "room_type_id", "room_number", "price", "phong_tam", "loai_phong_tam", "phong_bep", "loai_phong_bep","gia_dien", "gia_nuoc", "tien_ich_khac"]
	int_fields = ["room_type_id", "room_number", "price", "phong_tam", "phong_bep", "gia_dien", "gia_nuoc", "dien_tich", "loai_phong_tam", "loai_phong_bep"]
	form_checkbox = ["chung_chu", "nong_lanh", "dieu_hoa", "ban_cong"]
	for attr in form_attrs:
		try:
			room_data[attr] = data_form[attr]
			if(room_data[attr] == ""):
				res["msg"] = "Thieu truong can thiet"
				return jsonify(res)
		except:
			res["msg"] = "Thieu truong can thiet"
			return jsonify(res)
	for f in int_fields:
		try:
			room_data[f] = int(room_data[f])
		except:
			res["msg"] = "Thong tin khong hop le"
			return jsonify(res)

	for attr in form_checkbox:
		try:
			x = data_form[attr]
			if(x == "on"):
				room_data[attr] = True
			else:
				room_data[attr] = False
		except:
			room_data[attr] = False
	status, msg = update_post(resp, room_data)
	res["status"] = status
	res["msg"] = msg
	return jsonify(res)

@owner_bp.route("/post/update/<int:id>")
@is_owner
def route_update_post(id):
	status, resp = get_post(id, current_user.id)
	if(status != "success"):
		abort(403)
	if(resp.pending == True):
		abort(403)
	return render_template("owner/updatepost.html", post = resp, title="Sửa bài đăng")

@owner_bp.route("/api/post/delete/<int:id>")
@is_owner
def api_delete_post(id):
	res = {}
	res["status"] = "error"
	res["msg"] = "co loi xay ra"
	status, msg = delete_post(id, current_user.id)
	res["status"] = status
	res["msg"] = msg
	return jsonify(res)

@owner_bp.route("/post/")
@is_owner
def route_list_room():
	posts = get_posts(current_user.id)
	return render_template("owner/room.html",posts = posts, title="Danh sách bài đăng")

@owner_bp.route("/api/post/changestatus/<int:id>")
@is_owner
def api_change_status(id):
	res = {}
	res["status"] = "error"
	res["textNodeValue"] = ""
	res["msg"] = "co loi xay ra"
	status, msg, textValue = update_status(id, current_user.id)
	res["status"] = status
	res["msg"] = msg
	res["textNodeValue"] = textValue
	return jsonify(res)

@owner_bp.route("/profile")
@owner_bp.route("/profile/<username>")
@is_owner
def profile(username=None):
	if(username == None):
		username = current_user.username
	msg, owner = get_owner_by_username(username)
	if(msg == "error"):
		abort(404)
	return render_template("owner/profile.html", owner = owner, title="Hồ sơ người dùng")