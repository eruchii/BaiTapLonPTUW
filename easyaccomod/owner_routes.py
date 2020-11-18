from flask import *
from easyaccomod import app
from flask_login import login_user, current_user
from easyaccomod.owner_models import Owner, User
from functools import wraps
from easyaccomod.owner_db import check_user, add_user, change_password

owner_bp = Blueprint("owner", __name__, template_folder='templates/owner')

def is_owner(f):
	@wraps(f)
	def decorated_func(*args, **kwargs):
		if(current_user.is_anonymous):
			abort(403)
			return
		if(current_user.role_id == 2):
			abort(403)
			return
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
	return render_template("owner/login.html")

@owner_bp.route("/changepassword")
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