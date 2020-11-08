from flask import Blueprint
from easyaccomod.admin.forms import LoginForm, RegistrationForm
from easyaccomod import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from easyaccomod.models import User

admin = Blueprint('admin', __name__)
# dummy data
posts = [
    {
        'author_username': 'eruchii',
        'title': 'eruchii title',
        'content': 'eruchii content',
        'date_posted': '06 11 2020',
        'address': '144 duong-phuong-tinh',
        'type': 'house',
        'room_count': '3',
        'area': '120m2',
        'infrastructure': 'something.... full feature ...',
        'extension': 'air conditioner',
        'count': 1234,
        'pending': True
    },
    {
        'author_username': 'honest',
        'title': 'honest title',
        'content': 'honest content',
        'date_posted': '07 11 2020',
        'address': '212 duong-phuong-tinh-2',
        'type': 'mini',
        'room_count': '2',
        'area': '30m2',
        'infrastructure': 'somthing ... vv',
        'extension': '',
        'count': 2256,
        'pending': False
    }
]

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
            flash("Login Unsucccessful. Please check for email and password", "danger")
    return render_template("login.html", title="Login", form=form)

@admin.route("/account")
@login_required
def account():
    return f"User {current_user.username} role_id {current_user.role_id}"

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@admin.route("/admin_home")
@login_required
def admin_home():
    if current_user.role_id != 1 or current_user.status_confirm != 1:
        abort(403)
    return render_template("admin_home.html", posts=posts)
