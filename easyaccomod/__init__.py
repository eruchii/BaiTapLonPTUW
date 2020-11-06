from flask import Flask
from flask_login import login_manager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '80e63eb7f7af4b8bb32edc7839994cb2'
# mysql+pymysql://root:''@localhost/easyaccomod
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/easyaccomod' # test

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from easyaccomod import routes