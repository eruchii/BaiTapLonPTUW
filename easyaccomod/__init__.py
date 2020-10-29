from flask import Flask
from flask_login import login_manager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '80e63eb7f7af4b8bb32edc7839994cb2'
# mysql+pymysql://root:''@localhost/accommodation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from easyaccomod import routes