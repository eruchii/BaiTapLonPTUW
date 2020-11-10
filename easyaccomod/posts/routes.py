from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from easyaccomod import db
from easyaccomod.models import Post
from easyaccomod.posts.forms import PostForm

from easyaccomod.admin.utils import createPostByAdmin

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm(pending=True)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        room_id = form.room_id.data
        pending = form.pending.data
        print(title, " ", content, " ", room_id, " ", pending)
        createPostByAdmin(title=title, content=content, room_id=room_id)
        flash(f"Post has been created by { current_user.username }" , "success")
        return redirect(url_for('admin.admin_home'))
    return render_template("posts/create_post.html", title="New Post", form=form)

@posts.route("/post")
@login_required
def post():
    if current_user.role_id == 1:
        posts = Post.query.all()
        return render_template("posts/post.html", title="Manage Post", posts=posts)
    else:
        abort(403)