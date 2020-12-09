from flask import *
from easyaccomod import app
from flask_login import login_user, current_user, logout_user
from easyaccomod.owner_models import Owner, User
from functools import wraps
from easyaccomod.owner_db import check_user, add_user, change_password

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
	return render_template("owner/register.html")

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
	return render_template("owner/login.html")

@owner_bp.route("/changepassword")
@is_owner
def changepassword():
	return render_template("owner/changepassword.html")

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
	user = Owner.query.all()[int(id)]
	login_user(user, remember=True)
	return jsonify({"status":"ok"})

@owner_bp.route("/")
@is_owner
def home():
	return render_template("owner/home.html")

@owner_bp.route("/notification")
@is_owner
def notification():
	return render_template("owner/notification.html")

@owner_bp.route("/logout")
@is_owner
def logout():
	logout_user()
	return redirect(url_for("owner.login"))

@owner_bp.route("/room/create")
@is_owner
def create_new_room():
	return render_template("owner/createroom.html")

@owner_bp.route("/api/room/create", methods=["POST"])
@is_owner
def api_create_new_room():
	res = {}
	res["status"] = "error"
	res["msg"] = ""
	data_form = request.form
	img = request.files.getlist("image")
	print(len(img))
	print(data_form)
	print(img)
	form_attrs = ["city", "district", "ward", "info", "room_type_id", "room_number", "price", "phong_tam", "phong_bep", "gia_dien", "gia_nuoc"]
	for attr in form_attrs:
		try:
			x = data_form[attr]
			if(x == ""):
				res["msg"] = "Thieu truong can thiet"
				print(attr)
				return jsonify(res)
		except:
			print(attr)
			res["msg"] = "Thieu truong can thiet"
			return jsonify(res)
	
	print(len(img))
	if(len(img) < 3):
		res["msg"] = "Toi thieu 3 anh"
		return jsonify(res)
	res["status"] = "success"
	res["msg"] = "ok"
	return jsonify(res)