from flask import flash
from datetime import datetime
from easyaccomod import db, bcrypt
from easyaccomod.models import User, Post


def addUserByAdmin(username, password, email):
    """
        function: add user by admin -> status_confirm = 1 : OK
        user is added to the user table immediately with status "OK"
        should be used : add renter, force add renter by admin, force add owner by admin or add admin to table user
    """
    tmpUser = User.query.filter_by(username=username).first()
    if tmpUser:
        flash("Exist User", "danger")
        print("Exist User")
    else :
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        owner = User(username=username, email=email, password=hashed_password, role_id=3, status_confirm=1)
        db.session.add(owner)
        db.session.commit()
        return owner.id

def addUserByOwner(username, password, email):
    """
        function:: add user by owner : -> add a owner to table user, but status = WAIT
        para password : should be plaintext
        para email: unique same owner.email
        ---- return id of user added ----
    """
    tmpUser = User.query.filter_by(username=username).first()
    if tmpUser:
        flash("Exist User", "danger")
        print("Exist User")
        return (False)
    else :
        hash_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        owner = User(username=username, email=email, password=hash_pw, role_id=3, status_confirm=2)
        db.session.add(owner)
        db.session.commit()
        return owner.id

def createPostByAdmin(title, content, room_id, admin_id):
    """
        function should be used by admin. pls check role_id before use it
        post created by admin// auto pending = True : da dc xu ly xong r
        para :: admin_id => call by admin and get 'current_id' of admin 
    """
    post = Post(title=title, content=content, room_id=room_id, pending=True, user_id=admin_id) # pending = True -> xly xong r
    post.date_posted = datetime.utcnow()
    db.session.add(post)
    db.session.commit()
    

def deletePostByID(post_id):
    """
        function: delete post, should be used by admin
        pls check role_id before used it
    """
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash(f"xoa bai thanh cong", "info")
