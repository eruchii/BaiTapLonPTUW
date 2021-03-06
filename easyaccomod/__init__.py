import os
import celery
from gevent import monkey
monkey.patch_all()
from flask import Flask
from flask_login import login_manager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_mail import Mail, Message
from easyaccomod.flask_celery import make_celery
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = '80e63eb7f7af4b8bb32edc7839994cb2'
#mysql+pymysql://root:''@localhost/easyaccomod
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/easyaccomod'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CELERY_BROKER_URL'] = 'redis://0.0.0.0:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'db+sqlite:///db.sqlite3'

celery = make_celery(app=app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)

# login_view :: The name of the view to redirect to when the user needs to log in.
# 'login' is function of route
# or this can be an absolute URL as well <if your authentication machinery is external to your application>
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
mail = Mail(app)

# from easyaccomod import routes
# Blueprint :: import
from easyaccomod.owner_routes import owner_bp
from easyaccomod.chat import chat_bp
from easyaccomod.main.routes import main
from easyaccomod.admin.routes import admin
from easyaccomod.posts.routes import posts
from easyaccomod import renter_views
from easyaccomod.renter_views import renter_bp
from easyaccomod.errors.handlers import errors

# register Blueprint
app.register_blueprint(owner_bp, url_prefix = '/owner')
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(posts)
app.register_blueprint(renter_bp,url_prefix= "/renter")
app.register_blueprint(errors)