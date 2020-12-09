from easyaccomod import app
from easyaccomod.chat import socketio
if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	socketio.run(app, host="0.0.0.0", debug=True)