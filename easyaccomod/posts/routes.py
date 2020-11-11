from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from easyaccomod import db
from easyaccomod.models import Post
from easyaccomod.posts.forms import PostForm

from easyaccomod.admin.utils import checkRoomExist, createPostByAdmin

posts = Blueprint('posts', __name__)

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
                print(title, " ", content, " ", room_id, " ", pending)
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

@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash(f"Your post has been deleted by {current_user.username}!", "success")
        return redirect(url_for("posts.post"))
    else:
        abort(403)