from flask.helpers import url_for
from easyaccomod.forms import LoginForm, RegistrationForm
from easyaccomod import app
from flask import render_template, redirect

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    # tao form nhung chua xu ly dang ky
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # tao form nhung chua xu ly dang nhap
    form = LoginForm()
    if form.validate_on_submit():
        # xu ly dang nhap tai day
        return redirect(url_for("home"))
    return render_template("login.html", form=form)
