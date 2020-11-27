from flask.json import jsonify
from easyaccomod.admin.utils import *
from flask import Blueprint
from easyaccomod.admin.forms import LoginForm, RegistrationForm, UpdateAccountForm
from easyaccomod import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort, Response
from flask_login import login_user, current_user, logout_user, login_required
## import models
from easyaccomod.models import User
from easyaccomod.owner_models import *

admin = Blueprint('admin', __name__)

@admin.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # admin
        if int(form.role.data) == 1:
            flash("Admin can not res... Please check the role!", "warning")
        # renter
        elif int(form.role.data) == 2:
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, role_id=2, status_confirm=1)
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created! You are now able to login without waiting for approval.", "success")
        # owner
        elif int(form.role.data) == 3:
            # eruchii: redirect to new form
            pass
        else :
            flash("Something went wrong, please check your role!", "danger")
        return redirect(url_for('admin.login'))
    return render_template("register.html", title="Register",form=form)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and (user.status_confirm == 1) and (user.role_id == 2) :
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and (user.status_confirm == 1) and (user.role_id == 1) :
            login_user(user, remember=form.remember.data)
            flash (f"Login successful! Welcome admin! {user.username}", "success") 
            return redirect(url_for("admin.admin_home"))
        else:
            flash("Login Unsucccessful. Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form)

@admin.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_user_picture(current_user.username, form.picture.data)
            current_user.image_file = picture_file
        if form.new_password.data == form.confirm_new_password.data:
            hash_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hash_password
        db.session.commit()
        flash("Your Account has been updated!", "success")
        return redirect(url_for('admin.account'))
    elif request.method == "GET":
        flash("You must type password to update account!", "info")
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("admin/account.html", title="Account", image_file=image_file, form=form)   

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@admin.route("/admin-home")
@login_required
def admin_home():
    if current_user.role_id != 1 or current_user.status_confirm != 1:
        abort(403)
    rooms = Room.query.all()
    return render_template("admin_home.html", rooms=rooms)

@admin.route("/manage-user", methods=["GET", "POST"])
@login_required
def manage_user():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        rolename = request.args.get('rolename', 'user', type=str)
        users = []
        if rolename == "user":
            users = User.query.all()
        elif rolename == "owner":
            users = User.query.filter_by(role_id=3).all()
        elif rolename == "admin":
            users = User.query.filter_by(role_id=1).all()
        return render_template("admin/manage_user.html", title="Manage User", users=users, rolename=rolename)
    else:
        abort(403)    
    
@admin.route("/owner/accept", methods=["GET", "POST"])
@login_required
def new_accept_owner():
    data = request.get_json()
    print(data["user_id"])
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xra"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            acceptOwner(data["user_id"])
            own = User.query.filter_by(id=data["user_id"]).first()
            resp["status"] = "success"
            resp["msg"] = f"Accept owner with username: {own.username}, status: {own.confirms.name}"
            resp["owner_status_confirm"] = own.confirms.name
            return jsonify(resp)
    except:
        return jsonify(resp)
    
@admin.route("/owner/reject", methods=["GET", "POST"])
@login_required
def new_reject_owner():
    data = request.get_json()
    print(data["user_id"])
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xay ra"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            own_id = rejectUser(data["user_id"])
            if own_id != -1:
                own = User.query.filter_by(id=own_id).first()
                resp["status"] = "success"
                resp["msg"] = f"Reject owner with username: {own.username}, status: {own.confirms.name}"
                resp["owner_status_confirm"] = own.confirms.name
            return jsonify(resp)
    except:
        return jsonify(resp)

@admin.route("/find/user", methods=["GET", "POST"])
@login_required
def find_user():
    strr = request.args.get('searchname', type=str)
    if strr:
        users = findUser(strr)
        print(users)
        return render_template("admin/manage_user.html", users=users)
    else :
        abort(Response('Hello World'))
# @admin.route("/manage-user/<int:user_id>/accept", methods=["GET","POST"])
# @login_required
# def accept_owner(user_id):
#     if current_user.role_id == 1 and current_user.status_confirm == 1:
#         rolename = request.args.get('rolename', 'user', type=str)
#         if checkUserExist(user_id=user_id):
#             acceptOwner(user_id)
#             flash(f"Owner has been accepted by {current_user.username}!", "success")
#             return redirect(url_for("admin.manage_user", rolename=rolename))
#     else:
#         abort(403)

# @admin.route("/manage-user/<int:user_id>/reject", methods=["GET", "POST"])
# @login_required
# def reject_owner(user_id):
#     if current_user.role_id == 1 and current_user.status_confirm == 1:
#         rolename = request.args.get('rolename', 'user', type=str)
#         if checkUserExist(user_id=user_id):
#             rejectUser(user_id)
#             flash(f"Owner has been rejected by {current_user.username}!", "success")
#             return redirect(url_for("admin.manage_user", rolename=rolename))
#     else:
#         abort(403)


###########################################################################

@admin.route("/api/test/<int:user_id>", methods=["GET", "POST"])
def testAPI(user_id):
    acceptOwner(user_id)
    return jsonify({"ans":"OK"})