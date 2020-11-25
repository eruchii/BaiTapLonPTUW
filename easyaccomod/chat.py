from flask_socketio import SocketIO, emit, disconnect, send
from flask import *
from easyaccomod import app, db, socketio
from flask_login import current_user
from functools import wraps
from easyaccomod.models import Message, User
from sqlalchemy import or_, and_
from datetime import datetime


chat_bp = Blueprint("chat", __name__)
clients = {}

def can_send_msg(f):
	@wraps(f)
	def decorated_func(*args, **kwargs):
		if(current_user.is_anonymous):
			abort(403)
			return
		return f(*args, **kwargs)
	return decorated_func

def send_msg_to_user(recv, msg, sender=False):
	status = True
	if not sender:
		status, resp_msg = add_msg(recv, msg)
	try:
		client = clients[recv]
		if(status):
			data = {
				"sender":current_user.username, "msg":msg, "date":datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "type":1, 
				"img":"https://ptetutorials.com/images/user-profile.png"
			}
			if(sender):
				data["type"] = 0
			socketio.emit("new msg", data, room=client)
	except:
		pass

def add_msg(recv, msg):
	recv_user = User.query.filter_by(username=recv).first()
	if not recv_user:
		return (False, "Không tồn tại người nhận.")
	try:
		new_msg = Message(sender=current_user.username, receiver=recv, content=msg)
		db.session.add(new_msg)
		db.session.commit()
		return (True, "Thanh cong")
	except:
		return (False, "Khong thanh cong")

def load_msg(sender, recv):
	msgs = Message.query.filter( 
		((Message.sender == recv) & (Message.receiver == sender)) |  
		((Message.sender == sender) & (Message.receiver == recv))
	)
	res = []
	for m in msgs:
		msg = {}
		msg["id"] = m.id
		msg["partner"] = recv
		msg["msg"] = m.content
		msg["type"] = 0
		msg["img"] = "https://ptetutorials.com/images/user-profile.png"
		msg["date"] = m.date_created.strftime("%m/%d/%Y, %H:%M:%S")
		if(m.receiver == sender):
			msg["type"] = 1
		res.append(msg)
		db.session.flush()
	db.session.commit()
	return res

@socketio.on("load msg")
@can_send_msg
def load_msg_his(data):
	msgs = load_msg(current_user.username, data["recv"])
	socketio.emit("chat log", msgs, room=clients[current_user.username])

@socketio.on("send msg")
@can_send_msg
def send_msg(data):
	send_msg_to_user(current_user.username, data["msg"], sender=True)
	send_msg_to_user(data["recv"], data["msg"])
	seen_msg(data["recv"])

@can_send_msg
def seen_msg(target):
	msgs = Message.query.filter((Message.sender == target) & (Message.receiver == current_user.username) & (Message.seen==False))
	for m in msgs:
		m.seen=True
		db.session.flush()
	db.session.commit()	
	
@socketio.on("connected")
@can_send_msg
def connected():
	clients[current_user.username] = request.sid

def load_people(sender):
	ppl = Message.query.filter(or_(Message.receiver==sender,Message.sender==sender))
	res = []
	for i in ppl:
		res.append(i.sender)
		res.append(i.receiver)
	res = set(res)
	if sender in res:
		res.remove(sender)
	return list(res)

def load_latest_msg(sender, recv):
	msgs = Message.query.filter( 
		((Message.sender == recv) & (Message.receiver == sender)) |  
		((Message.sender == sender) & (Message.receiver == recv))
	)
	if(msgs.count() == 0):
		resp = {}
		resp["id"] = -1
		resp["username"] = recv
		resp["sender"] = ""
		resp["receiver"] = ""
		resp["msg"] = ""
		resp["img"] = "https://ptetutorials.com/images/user-profile.png"
		resp["date"] = ""
		resp["new_msg"] = 0
		return resp
	latest_msg = msgs[-1]
	resp = {}
	resp["id"] = latest_msg.id
	resp["username"] = recv
	resp["sender"] = latest_msg.sender
	resp["receiver"] = latest_msg.receiver
	resp["msg"] = latest_msg.content
	resp["img"] = "https://ptetutorials.com/images/user-profile.png"
	resp["date"] = latest_msg.date_created.strftime("%m/%d/%Y, %H:%M:%S")
	
	new_msgs = Message.query.filter((Message.sender == recv) & (Message.receiver == sender) & (Message.seen == False))
	resp["new_msg"] = new_msgs.count()

	return resp

@socketio.on("load list people")
@can_send_msg
def load_list_people():
	ppl = load_people(current_user.username)
	resp = []
	for p in ppl:
		res = load_latest_msg(current_user.username, p)
		resp.append(res)
	resp.sort(key= lambda x: x["id"], reverse=True)
	socketio.emit("loaded list people", resp, room = clients[current_user.username])

@chat_bp.route("/")
@can_send_msg
def index():
	return render_template("chat.html", async_mode=socketio.async_mode)

@socketio.on("search user")
def search_user(data):
	search = data["search"]
	search_query = "{}%".format(search)
	users = User.query.filter(User.username.like(search_query))
	if(users.count == 0):
		return
	res = []
	for user in users:
		r = load_latest_msg(current_user.username, user.username)
		res.append(r)
	res.sort(key= lambda x: (x["id"]*-1, x["username"]))
	socketio.emit("loaded list people", res, room = clients[current_user.username])

