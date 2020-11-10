from flask import request, abort, flash
from flask_login import current_user, login_required
from datetime import datetime
from easyaccomod import db, bcrypt
from easyaccomod.models import User, Post


@login_required
def addUserByAdmin(username, password, email):
    if current_user.role_id == 1:
        tmpUser = User.query.filter_by(username=username).first()
        if tmpUser:
            flash("Exist User", "danger")
            print("Exist User")
        else :
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            owner = User(username=username, email=email, password=hashed_password, role_id=3, status_confirm=1)
            db.session.add(owner)
            db.session.commit()
    else :
        abort(403)

@login_required
def createPostByAdmin(title, content, room_id):
    if current_user.role_id == 1 or current_user.role_id == 3:
        print(current_user.role_id)
        post = Post(title=title, content=content, room_id=room_id, pending=True, user_id=current_user.id)
        post.date_posted = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
    else:
        abort(403)
    