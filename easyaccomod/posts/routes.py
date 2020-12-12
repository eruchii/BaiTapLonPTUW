from datetime import timedelta, datetime, date
from flask import Blueprint, jsonify
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from easyaccomod import db
from easyaccomod.models import *
from easyaccomod.owner_models import *
from easyaccomod.posts.forms import PostForm, RoomForm, UpdatePostForm

from easyaccomod.admin.utils import checkRoomExist, createPostByAdmin, save_room_picture, sendNotification

posts = Blueprint('posts', __name__)

@posts.route("/post/accept", methods=['POST'])
@login_required
def new_accept_post():
    data = request.get_json()
    print(data)
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xay ra"
    resp["post_pending"] = "False"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            post = Post.query.get_or_404(data["post_id"])
            post.pending = True # True -> accept post
            sendNotification(receiver=post.author.id, title="Accept Post", msg=f"The post with id {post.id} and author : {post.author.username} has been accepted by {current_user.username}")
            db.session.commit()
            resp["status"] = "success"
            resp["msg"] = "Accepted Post - post_id = {}".format(data["post_id"])
            resp["post_pending"] = "True"
        return jsonify(resp)
    except :
        return jsonify(resp)

@posts.route("/post/reject", methods=["GET", "POST"])
@login_required
def new_reject_post():
    data = request.get_json()
    print(data)
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xra"
    resp["post_pending"] = "True"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            post = Post.query.get_or_404(data["post_id"])
            post.pending = False
            sendNotification(receiver=post.author.id, title="Reject Post", msg=f"The post with id {post.id} and author : {post.author.username} has been REJECTED by {current_user.username}")
            db.session.commit()
            resp["status"] = "success"
            resp["msg"] = f"Rejected Post - post_id = {data['post_id']}"
            resp["post_pending"] = "False"
        return jsonify(resp)
    except:
        return jsonify(resp)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.role_id == 1:
        form_title = "Create Post"
        form = PostForm(pending=True)
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            room_id = form.room_id.data
            date_out = form.date_out.data
            pending = form.pending.data
            if checkRoomExist(room_id=room_id):
                createPostByAdmin(title=title, content=content, room_id=room_id, date_out=date_out, admin_id=current_user.id)
                flash(f"Post has been created by { current_user.username }" , "success")
                return redirect(url_for('posts.post'))
            else :
                flash(f"Room does not exist!", "danger")
                return redirect(url_for('posts.new_post'))
        elif request.method == "GET":
            room_id = request.args.get("room", type=int)
            if room_id:
                form.room_id.data = room_id
            time_delta = timedelta(days=30)
            today = datetime.utcnow().date()
            req = today + time_delta
            form.date_out.data = req
        return render_template("posts/create_post.html", title="New Post", form_title=form_title, form=form)
    else :
        abort(403)
    

@posts.route("/post")
@login_required
def post():
    if current_user.role_id == 1:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
        return render_template("posts/post.html", title="Manage Post", posts=posts)
    else:
        abort(403)

@posts.route("/post/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash(f"Post has been deleted by {current_user.username}!", "success")
        return redirect(url_for("posts.post"))
    else:
        abort(403)

@posts.route("/post/details/<int:post_id>", methods=["GET", "POST"])
@login_required
def view_post(post_id):
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        post = Post.query.get_or_404(post_id)
        if post:
            post.count_view += 1
            db.session.commit()
        return render_template("posts/view_post.html", title="View Post", post=post)

@posts.route("/post/update/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form_title = "Update Post"
    if current_user.role_id != 1 :
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.room_id = form.room_id.data
        post.date_posted = form.date_posted.data
        post.date_out = form.date_out.data
        post.pending = form.pending.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for('posts.view_post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.room_id.data = post.room_id
        form.date_posted.data = post.date_posted
        form.date_out.data = post.date_out
        form.pending.data = post.pending
    return render_template("posts/update_post.html", title="Update Post", form_title=form_title, form=form)

@posts.route("/manage-my-post")
@login_required
def manage_my_post():
    if current_user.status_confirm != 1 or current_user.role_id == 2:
        abort(403)
    else :
        user = User.query.get_or_404(current_user.id)
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(author=user).order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
        return render_template("posts/post.html", title="Manage My Post", posts=posts)

@posts.route("/room/new", methods=["GET", "POST"])  
@login_required
def new_room():
    if current_user.role_id == 1:
        form = RoomForm()
        if form.validate_on_submit():
            room = Room(user_id=current_user.id, 
                        city_code=form.city.data, 
                        district_id=form.district.data, 
                        ward_id=form.ward.data, 
                        info=form.info.data, 
                        room_type_id=form.room_type.data, 
                        room_number=form.room_number.data, 
                        price=form.price.data, 
                        chung_chu=form.chung_chu.data, 
                        phong_tam=form.phong_tam.data, 
                        nong_lanh=form.nong_lanh.data, 
                        phong_bep=form.phong_bep.data, 
                        dieu_hoa=form.dieu_hoa.data, 
                        ban_cong=form.ban_cong.data, 
                        gia_dien=form.gia_dien.data, 
                        gia_nuoc=form.gia_nuoc.data, 
                        tien_ich_khac=form.tien_ich_khac.data,
                        status=form.status.data)
            db.session.add(room)
            db.session.flush()
            list_img = []
            for file in form.image.data:
                file_name = save_room_picture(str(room.id), file)
                list_img.append(file_name)
            room_image = str(list_img)
            print(room_image)
            room.image = room_image
            db.session.commit()
            flash(f"add room ok with room_id = {room.id}", "success")
            return redirect(url_for('posts.room'))
        return render_template("posts/create_room.html", title="New Room", form=form)
    else :
        abort(403)
    
@posts.route("/room/update/<int:room_id>", methods=["GET", "POST"])
@login_required
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    if current_user.role_id == 2 or current_user.status_confirm != 1 or current_user != room.user:
        abort(403)
    else :
        form = RoomForm()
        if form.validate_on_submit():
            room.city_code=form.city.data
            room.district_id=form.district.data
            room.ward_id=form.ward.data
            room.info=form.info.data
            room.room_type_id=form.room_type.data
            room.room_number=form.room_number.data 
            room.price=form.price.data
            room.chung_chu=form.chung_chu.data
            room.phong_tam=form.phong_tam.data 
            room.nong_lanh=form.nong_lanh.data 
            room.phong_bep=form.phong_bep.data 
            room.dieu_hoa=form.dieu_hoa.data
            room.ban_cong=form.ban_cong.data 
            room.gia_dien=form.gia_dien.data 
            room.gia_nuoc=form.gia_nuoc.data 
            room.tien_ich_khac=form.tien_ich_khac.data
            room.status=form.status.data  
            list_img = []
            for file in form.image.data:
                file_name = save_room_picture(str(room.id), file)
                list_img.append(file_name)
            room_image = str(list_img)
            room.image = room_image
            db.session.commit()
            flash(f"Your room has been updated with room_id = {room.id}!", "success")
            return redirect(url_for('posts.view_room', room_id=room.id))
        elif request.method == "GET":
            form.city.choices = [(room.city.code, room.city.name)]
            form.info.data = room.info
            #form.room_type.data = (room.roomtype.id if room.roomtype else 0)
            form.room_number.data = room.room_number
            form.price.data = room.price
            form.chung_chu.data = room.chung_chu
            form.phong_tam.data = room.phong_tam
            form.nong_lanh.data = room.nong_lanh
            form.phong_bep.data = room.phong_bep
            form.dieu_hoa.data = room.dieu_hoa
            form.ban_cong.data = room.ban_cong
            form.gia_dien.data = room.gia_dien
            form.gia_nuoc.data = room.gia_nuoc
            form.tien_ich_khac.data = room.tien_ich_khac
            form.status.data = room.status
        return render_template('posts/update_room.html', form=form)

@posts.route("/room", methods=["GET"])
@login_required
def room():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        page = request.args.get('page', 1, int)
        rooms = Room.query.order_by(Room.id.desc()).paginate(page=page, per_page=5)
        return render_template("posts/room.html", title = "Room", rooms=rooms)
    else :
        abort(403)

@posts.route("/room/details/<int:room_id>", methods=["GET", "POST"])
@login_required
def view_room(room_id):
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        room = Room.query.get_or_404(room_id)
        return render_template("posts/view_room.html", title="View Room", room=room)

@posts.route("/manage-my-room", methods=["GET"])
@login_required
def manage_my_room():
    if current_user.status_confirm != 1 or current_user.role_id == 2:
        abort(403)
    else :
        us = User.query.get_or_404(current_user.id)
        page = request.args.get('page', 1, int)
        rooms = Room.query.filter_by(user=us).order_by(Room.id.desc()).paginate(page=page, per_page=5)
        return render_template("posts/room.html", title="Manage Room", rooms=rooms)

# @posts.route("/post/<int:post_id>/accept", methods=["GET", "POST"])
# @login_required
# def accept_post(post_id):
#     if current_user.id == 1 and current_user.status_confirm == 1:
#         post = Post.query.get_or_404(post_id)
#         post.pending = True # True -> accept post
#         db.session.commit()
#         flash(f"Post {post_id} has been accepted by {current_user.username}!", "success")
#         return redirect(url_for("posts.post"))
#     else :
#         abort(403)

# @posts.route("/post/<int:post_id>/reject", methods=["GET", "POST"])
# @login_required
# def reject_post(post_id):
#     if current_user.id == 1 and current_user.status_confirm == 1:
#         post = Post.query.get_or_404(post_id)
#         post.pending = False # False -> reject post -> post wait
#         db.session.commit()
#         flash(f"Post {post_id} has been rejected by {current_user.username}!", "success")
#         return redirect(url_for("posts.post"))
#     else :
#         abort(403)

@posts.route("/post/api")
def posttt():
    ans = []
    posts = Post.query.all()
    for post in posts:
        res = {"id":post.id, "title":post.title, "content":post.content, "room_id":post.room_id, "pending":post.pending, "date_created":post.date_created, "date_posted":post.date_posted, "date_out":post.date_out, "user_id":post.user_id}
        ans.append(res)
    return jsonify(ans)    