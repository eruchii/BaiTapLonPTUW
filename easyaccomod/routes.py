from easyaccomod.forms import LoginForm, RegistrationForm
from easyaccomod import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from easyaccomod.models import User

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template("register.html", title="Register",form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and (user.status_confirm == 1) :
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsucccessful. Please check for email and password", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))