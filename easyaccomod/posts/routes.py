from flask import Blueprint, jsonify
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from easyaccomod import db
from easyaccomod.models import Post
from easyaccomod.owner_models import *
from easyaccomod.posts.forms import PostForm, RoomForm, UpdatePostForm

from easyaccomod.admin.utils import checkRoomExist, createPostByAdmin

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
            db.session.commit()
            resp["status"] = "success"
            resp["msg"] = "xac nhan thanh cong post_id = {}".format(data["post_id"])
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
            db.session.commit()
            resp["status"] = "success"
            resp["msg"] = f"reject thanh cong, post_id = {data['post_id']}"
            resp["post_pending"] = "False"
        return jsonify(resp)
    except:
        return jsonify(resp)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.role_id == 1:
        form = PostForm(pending=True)
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            room_id = form.room_id.data
            pending = form.pending.data
            if checkRoomExist(room_id=room_id):
                createPostByAdmin(title=title, content=content, room_id=room_id, admin_id=current_user.id)
                flash(f"Post has been created by { current_user.username }" , "success")
                return redirect(url_for('posts.post'))
            else :
                flash(f"Room does not exist!", "danger")
                return redirect(url_for('posts.new_post'))
        return render_template("posts/create_post.html", title="New Post", form=form)
    else :
        abort(403)
    

@posts.route("/post")
@login_required
def post():
    if current_user.role_id == 1:
        posts = Post.query.all()
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
        return render_template("posts/view_post.html", title="View Post", post=post)

@posts.route("/post/update/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.role_id != 1 :
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.room_id = form.room_id.data
        post.date_posted = form.date_posted.data
        post.pending = form.pending.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for('posts.view_post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.room_id.data = post.room_id
        form.date_posted.data = post.date_posted
        form.pending.data = post.pending
    return render_template("posts/update_post.html", title="Update Post", form=form)

@posts.route("/room/new", methods=["GET", "POST"])
@login_required
def new_room():
    if current_user.role_id == 1:
        form = RoomForm()
        if form.validate_on_submit():
            print(form.city.data," ", form.district.data, " ", form.ward.data)
            print(form.info.data, " ",form.room_type.data, " ", form.room_number.data)
            print(form.price.data, " ", form.chung_chu.data, " ", form.nong_lanh.data, " ", form. dieu_hoa.data, " ", form.ban_cong.data)
            print(form.phong_tam.data, " ", form.phong_bep.data)
            print(form.gia_dien.data, " ", form.gia_nuoc.data)
            print(form.pending.data)
            print("===============")
            for file in form.image.data:
                print(file)
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
                        pending=form.pending.data)
            db.session.add(room)
            db.session.commit()
            flash(f"add room ok with room_id = {room.id}")
            return redirect(url_for('posts.room'))
        return render_template("posts/create_room.html", title="New Room", form=form)
    else :
        abort(403)
    
@posts.route("/room", methods=["GET"])
@login_required
def room():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        rooms = Room.query.all()
        return render_template("posts/room.html", title = "Room", rooms=rooms)
    else :
        abort(403)


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

# @posts.route("/post")
# @login_required
# def post():
#     ans = []
#     if current_user.role_id == 1:
#         posts = Post.query.all()
#         for post in posts:
#             res = {"id":post.id, "title":post.title, "content":post.content, "room_id":post.room_id, "pending":post.pending, "date_created":post.date_created, "date_posted":post.date_posted, "date_out":post.date_out, "user_id":post.user_id}
#             ans.append(res)
#         return jsonify({"posts":ans})