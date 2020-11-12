from flask import *
from easyaccomod import app
from flask_login import login_user, current_user
from easyaccomod.owner_models import Owner
from functools import wraps
from easyaccomod.owner_db import check_user, add_user

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
	return "cac"

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
	
@owner_bp.route("/fakelogin")
def fakelogin():
	user = Owner.query.all()[0]
	login_user(user, remember=True)
	return user.username