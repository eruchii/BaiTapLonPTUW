from flask_socketio import SocketIO, emit, disconnect, send
from flask import *
from easyaccomod import app, db
from flask_login import current_user
from functools import wraps

chat_bp = Blueprint("chat", __name__)
socketio = SocketIO(app)
clients = {}

def can_send_msg(f):
	@wraps(f)
	def decorated_func(*args, **kwargs):
		if(current_user.is_anonymous):
			abort(403)
			return
		return f(*args, **kwargs)
	return decorated_func

def send_msg_to_user(recv, msg):
	try:
		client = clients[recv]
	except:
		client = clients[current_user.username]
	socketio.emit("new msg", {"sender":current_user.username, "msg":msg}, room=client)

@socketio.on("send msg")
@can_send_msg
def send_msg(data):
	send_msg_to_user(data["recv"], data["msg"])
	
@socketio.on("connected")
@can_send_msg
def connected():
	clients[current_user.username] = request.sid

@chat_bp.route('/fakemsg', methods=["POST"])
@can_send_msg
def fakemsg():
	socketio.emit("send msg", {"sender":"nct", "msg":"hello"}, room=clients["nct1"])
	return jsonify({"status":"success"})

@chat_bp.route("/")
@can_send_msg
def index():
	for i in clients:
		print(i, clients[i])
	return render_template("chat.html", async_mode=socketio.async_mode)