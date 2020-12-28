from flask.json import jsonify
from easyaccomod.admin.utils import *
from flask import Blueprint
from easyaccomod.admin.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from easyaccomod import app, db, bcrypt, celery
from flask import render_template, redirect, url_for, flash, request, abort, Response
from flask_login import login_user, current_user, logout_user, login_required
## import models
from easyaccomod.models import *
from easyaccomod.owner_models import *
from easyaccomod.room_models import *

admin = Blueprint('admin', __name__)

@admin.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # admin
        if int(form.role.data) == 1:
            flash("Admin can not res... Please check the role!", "warning")
        # renter
        elif int(form.role.data) == 2:
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, role_id=2, status_confirm=1)
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created! You are now able to login without waiting for approval.", "success")
        # owner
        elif int(form.role.data) == 3:
            # eruchii: redirect to new form
            pass
        else :
            flash("Something went wrong, please check your role!", "danger")
        return redirect(url_for('admin.login'))
    return render_template("register.html", title="Register",form=form)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and (user.status_confirm == 1) and (user.role_id == 2) :
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and (user.status_confirm == 1) and (user.role_id == 1) :
            login_user(user, remember=form.remember.data)
            flash (f"Login successful! Welcome admin! {user.username}", "success") 
            return redirect(url_for("admin.admin_home"))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and (user.status_confirm == 1) and (user.role_id == 3) :
            login_user(user, remember=form.remember.data)
            flash(f"Đăng nhập thành công!", "success")
            return redirect(url_for('owner.home'))
        else:
            flash("Login Unsucccessful. Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form)

@admin.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_user_picture(current_user.username, form.picture.data)
            current_user.image_file = picture_file
        if form.new_password.data == form.confirm_new_password.data:
            hash_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hash_password
        db.session.commit()
        flash("Your Account has been updated!", "success")
        return redirect(url_for('admin.account'))
    elif request.method == "GET":
        flash("You must type password to update account!", "info")
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("admin/account.html", title="Account", image_file=image_file, form=form)   

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@admin.route("/admin-home")
@login_required
def admin_home():
    if current_user.role_id != 1 or current_user.status_confirm != 1:
        abort(403)
    else :
        posts = Post.query.order_by(Post.count_view.desc()).limit(15).all()
        return render_template("admin_home.html", posts=posts)

@admin.route("/manage-user", methods=["GET", "POST"])
@login_required
def manage_user():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        rolename = request.args.get('rolename', 'user', type=str)
        page = request.args.get('page', 1, type=int)
        sortby = request.args.get('sortby', 'desc', type=str)
        users = []
        if sortby == "asc" :
            if rolename == "user":
                users = User.query.order_by(User.id.asc()).paginate(page=page, per_page=15)
            elif rolename == "owner":
                users = User.query.filter_by(role_id=3).order_by(User.id.asc()).paginate(page=page, per_page=15)
            elif rolename == "admin":
                users = User.query.filter_by(role_id=1).order_by(User.id.asc()).paginate(page=page, per_page=15)
        elif sortby == "desc" :
            if rolename == "user":
                users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=15)
            elif rolename == "owner":
                users = User.query.filter_by(role_id=3).order_by(User.id.desc()).paginate(page=page, per_page=15)
            elif rolename == "admin":
                users = User.query.filter_by(role_id=1).order_by(User.id.desc()).paginate(page=page, per_page=15)
        return render_template("admin/manage_user.html", title="Manage User", users=users, rolename=rolename, page=page, sortby=sortby)
    else:
        abort(403)    
    
@admin.route("/owner/accept", methods=["GET", "POST"])
@login_required
def new_accept_owner():
    data = request.get_json()
    print(data["user_id"])
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xra"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            own = User.query.filter_by(id=data["user_id"]).first()
            if own :
                acceptOwner(data["user_id"])
                sendNotification(receiver=own.id, title="Accept User", msg=f"Tài khoản với username: {own.username} đã được duyệt bởi: {current_user.username}! Cám ơn bạn đã đồng hành cùng EasyAccomod Group!")
                resp["status"] = "success"
                resp["msg"] = f"Accept user with username: {own.username}, status: {own.confirms.name}"
                resp["owner_status_confirm"] = own.confirms.name
                return jsonify(resp)
            else :
                return jsonify(resp)
    except Exception as e:
        print(e)
        return jsonify(resp)
    
@admin.route("/owner/reject", methods=["GET", "POST"])
@login_required
def new_reject_owner():
    data = request.get_json()
    print(data["user_id"])
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xay ra"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            own_id = rejectUser(data["user_id"])
            if own_id != -1:
                own = User.query.filter_by(id=own_id).first()
                sendNotification(receiver=own.id, title="Reject User", msg=f"Tài khoản với username {own.username} đã bị từ chối bởi admin: {current_user.username}! Vui lòng liên hệ admin để biết thêm chi tiết.")
                resp["status"] = "success"
                resp["msg"] = f"Reject user with username: {own.username}, status: {own.confirms.name}"
                resp["owner_status_confirm"] = own.confirms.name
            return jsonify(resp)
    except:
        return jsonify(resp)

@admin.route("/find/user", methods=["GET", "POST"])
@login_required
def find_user():
    searchname = request.args.get('searchname', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 15
    if searchname:
        users = findUser(user_name=searchname, page=page, per_page=per_page)
        return render_template("admin/find_user.html", users=users, searchname=searchname)
    else :
        abort(Response('Hello World'))

@admin.route("/statistics", methods=["GET", "POST"])
@login_required
def statistics():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        if request.method == "GET":
            yearnow = datetime.utcnow().year
            ans = {}
            ans["data_post"] = get_data_post_in_a_year(year=yearnow)
            ans["data_user"] = get_data_user_register_in_a_year(year=yearnow)
            ans["label_post"] = f"Statistic post in {yearnow}"
            ans["label_user"] = f"Statistic user in {yearnow}"
            return render_template("admin/statistic.html", title="Statistic", ans=ans)
        elif request.method == "POST":
            data = request.get_json()
            ans = {}
            ans["data_post"] = get_data_post_in_a_year(year=data["year"])
            ans["data_user"] = get_data_user_register_in_a_year(year=data["year"])
            ans["label_post"] = f'Statistic post in {data["year"]}'
            ans["label_user"] = f'Statistic user in {data["year"]}'
            return jsonify(ans)
    else:
        abort(403)

@admin.route("/statistics/user", methods=["GET", "POST"])
@login_required
def statistics_user():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        view = request.args.get("view", "chart", type=str)
        ans = {}
        req = statistic_price_log()
        ans["data"] = req
        if view == "chart":
            return render_template("admin/statistic_user.html", title="Statistic User", ans=ans)
        else :
            abort(Response("View Table"))
    else:
        abort(403)


@admin.route("/statistic/post", methods=["GET", "POST"])
@login_required
def statistics_post():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        ans = {}
        cities = City.query.all()
        ls = []
        for city in cities:
            ls.append(city.name)
        ans["city"] = ls
        req = cac_tinh_duoc_xem_nhieu_nhat(5)
        ans["data"] = req
        return render_template("admin/statistic_post.html", title="Statistic Post", ans=ans)
    else:
        abort(403)

@admin.route("/api/statistic/province", methods=["POST"])
@login_required
def statistic_province():
    ans = {}
    ans["status"] = "error"
    ans["msg"] = "Co loi xay ra"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            data = request.get_json()
            req = cac_quan_duoc_xem_nhieu_nhat(data["province"], 5)
            if req[0] == "False":
                ans["status"] = "error"
                ans["msg"] = "Không tìm thấy tỉnh này!"
                return jsonify(ans)
            else:
                ans["status"] = "success"
                ans["msg"] = "Danh sách các quận trong trường data"
                ans["data"] = req
            return jsonify(ans)
    except:
        return jsonify(ans)
    

@admin.route("/statistic/room", methods=["GET", "POST"])
@login_required
def statistics_room():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        ans = {}
        ans["xLabel"] = "Khoảng giá (triệu đồng)"
        ans["yLabel"] = "Số lượng (căn)"
        req = statistic_cost_room()
        ans["data_cost_room"] = req
        ans["xLength"] = len(req)
        ans["xLabel1"] = "Tỉnh"
        ans["yLabel1"] = "Số lượng"
        req1 = most_city_room(5)
        ans["data_x_1"] = req1[0]
        ans["data_y_1"] = req1[1]
        print(ans["data_x_1"], " ", ans["data_y_1"])
        return render_template("admin/statistic_room.html", title="Statistic Room", ans=ans)
    else:
        abort(403)

@admin.route("/confirm-comment")
@login_required
def confirm_comment():
    if current_user.role_id != 1 or current_user.status_confirm != 1:
        abort(403)
    else :
        page = request.args.get('page', 1, type=int)
        per_page = 20
        comments = Comment.query.order_by(Comment.date_created.desc()).paginate(page=page, per_page=per_page)
        return render_template("admin/confirm_comment.html", comments=comments)

@admin.route("/confirm-comment-post")
@login_required
def confirm_comment_post():
    if current_user.role_id != 1:
        abort(403)
    else :
        post_id = request.args.get("post_id")
        post = Post.query.filter_by(id=post_id).first_or_404()
        comments = post.comments
        return render_template("admin/comment_post.html", comments=comments)

@admin.route("/comment/accept", methods=["GET", "POST"])
@login_required
def acceptComment():
    data = request.get_json()
    print(data["comment_id"])
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xay ra"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            cmt_id = accept_comment(data["comment_id"])
            if cmt_id!= -1:
                comment = Comment.query.filter_by(id=cmt_id).first()
                resp["status"] = "success"
                resp["msg"] = f"Accept comment of user: {comment.user.username} with post_id: {comment.post.id}, status comment: {comment.status}"
                if comment.status == True:
                    resp["comment_status"] = "True"
                else:
                    resp["comment_status"] = "False"
            return jsonify(resp)
    except Exception as e:
        print(e)
        return jsonify(resp)

@admin.route("/comment/reject", methods=["GET", "POST"])
@login_required
def rejectComment():
    data = request.get_json()
    print(data["comment_id"])
    resp = {}
    resp["status"] = "error"
    resp["msg"] = "co loi xay ra"
    try:
        if current_user.role_id == 1 and current_user.status_confirm == 1:
            cmt_id = reject_comment(data["comment_id"])
            if cmt_id!= -1:
                comment = Comment.query.filter_by(id=cmt_id).first()
                resp["status"] = "success"
                resp["msg"] = f"Reject comment of user: {comment.user.username} with post_id: {comment.post.id}, status comment: {comment.status}"
                if comment.status == True:
                    resp["comment_status"] = "True"
                else:
                    resp["comment_status"] = "False"
            return jsonify(resp)
    except Exception as e:
        print(e)
        return jsonify(resp)

@admin.route("/admin-notifications")
@login_required
def admin_notifications():
    if current_user.role_id == 1 and current_user.status_confirm == 1:
        notifications = AdminNotification.query.order_by(AdminNotification.id.desc()).all()
        if notifications:
            for notification in notifications:
                notification.seen = True
            db.session.commit()
        return render_template("admin/admin_notification.html", notifications=notifications)
    else :
        abort(403)

@admin.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("admin/user_post.html", posts=posts, user=user)

@admin.route('/reset-password', methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        print(user.id, user.username, user.email)
        email_data = {
            'user_email': user.email,
            'body': f'''To reset your password, visit the following link:
{url_for('admin.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
        }
        # print(email_data)
        send_reset_email.delay(data=email_data)
        flash(f'An email has been sent', 'info')
        return redirect(url_for('admin.login'))
    return render_template("admin/reset_password.html", title="Reset Password", form=form)

@admin.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('admin.reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_token.html', title='Reset Password', form=form)


# @admin.route("/manage-user/<int:user_id>/accept", methods=["GET","POST"])
# @login_required
# def accept_owner(user_id):
#     if current_user.role_id == 1 and current_user.status_confirm == 1:
#         rolename = request.args.get('rolename', 'user', type=str)
#         if checkUserExist(user_id=user_id):
#             acceptOwner(user_id)
#             flash(f"Owner has been accepted by {current_user.username}!", "success")
#             return redirect(url_for("admin.manage_user", rolename=rolename))
#     else:
#         abort(403)

# @admin.route("/manage-user/<int:user_id>/reject", methods=["GET", "POST"])
# @login_required
# def reject_owner(user_id):
#     if current_user.role_id == 1 and current_user.status_confirm == 1:
#         rolename = request.args.get('rolename', 'user', type=str)
#         if checkUserExist(user_id=user_id):
#             rejectUser(user_id)
#             flash(f"Owner has been rejected by {current_user.username}!", "success")
#             return redirect(url_for("admin.manage_user", rolename=rolename))
#     else:
#         abort(403)


###########################################################################

@admin.route("/api/test/<int:user_id>", methods=["GET", "POST"])
def testAPI(user_id):
    acceptOwner(user_id)
    return jsonify({"ans":"OK"})