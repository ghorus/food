
from flask import abort,Blueprint,flash,redirect,render_template,request,url_for
from flask_login import login_user,login_required,logout_user,current_user
from flask_mail import Message
from foods import app, bcrypt, db, mail, socketio
from foods.models import Food_Post_Upload,Post,Profile_Pic_Upload,User
from foods.users.forms import (LoginForm,PostForm,RegistrationForm,RequestResetForm,
                                         ResetPasswordForm,UpdateAccountForm)
from werkzeug.utils import secure_filename

users = Blueprint('users',__name__)

@users.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic = form.picture.data
            sec_fn = secure_filename(pic.filename)
            if len(current_user.uploads) == 0:
                upload = Profile_Pic_Upload(filename=sec_fn,data=pic.read(),pic_owner=current_user)
                db.session.add(upload)
                db.session.commit()
            else:
                Profile_Pic_Upload.query.filter_by(user_id=current_user.id).delete()
                db.session.commit()
                upload = Profile_Pic_Upload(filename=sec_fn,data=pic.read(),pic_owner=current_user)
                db.session.add(upload)
                db.session.commit()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        # redirect instead of going to return render template to avoid another post request 
        # when reloading page
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    user_pic = Profile_Pic_Upload.query.filter_by(user_id=current_user.id).first()
    return render_template('users/account.html',form=form,image_file = user_pic, title='Account')

@users.route('/post/<post_id>/delete',methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    if post.uploads:
        foodPic = Food_Post_Upload.query.filter_by(post_id=post_id).first()
        db.session.delete(foodPic)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.','success')
    return redirect(url_for('main.home'))

@users.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password.','danger')
    return render_template('users/login.html',form=form,title='Login')

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post( author=current_user,city=form.city.data,content=form.content.data,
                    name=form.name.data,rating=form.rating.data, title=form.title.data)
        db.session.add(post)
        db.session.commit()
        if form.picture.data:
            pic = form.picture.data
            sec_fn = secure_filename(pic.filename)
            upload = Food_Post_Upload(filename=sec_fn,data=pic.read(),belongs_to_post=post)
            db.session.add(upload)
            db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('users/create_post.html',title='New Post',form=form)

@users.route('/post/<post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', title=post.title, post=post)

@users.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        totalUsers = len(User.query.all())
        socketio.emit('total users',totalUsers)
        flash('Your account has been created.','success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html',form=form,title='Register')

@users.route('/reset_password',methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('An email has been sent with instructions to reset your password.','success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html',form = form,title="Reset Password")

@users.route('/reset_password/<token>',methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That token is invalid or expired.','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated.','success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html',form = form,title="Reset Password")

def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='nguyen.victor4@gmail.com',recipients=[user.email])
    msg.body = f'''
    To reset, please click on the following link:
    {url_for('users.reset_token',salt='something',token=token,_external=True)}
    <h1>HEY WHATS GOOD</h1>
    If you didn't make this request, then you can simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

@users.route('/post/<post_id>/update',methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.city = form.city.data
        post.content = form.content.data
        post.name = form.name.data
        post.rating = form.rating.data
        post.title = form.title.data
        db.session.commit()
        if form.picture.data:
            pic = form.picture.data
            if len(post.uploads) == 0:
                upload = Food_Post_Upload(filename=pic.filename,data=pic.read(),belongs_to_post=post)
                db.session.add(upload)
                db.session.commit()
            else:
                Food_Post_Upload.query.filter_by(post_id=post.id).delete()
                db.session.commit()
                upload = Food_Post_Upload(filename=pic.filename,data=pic.read(),belongs_to_post=post)
                db.session.add(upload)
                db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('users.post',post_id=post.id))
    elif request.method == 'GET':
        form.city.data = post.city
        form.content.data = post.content
        form.name.data = post.name
        form.rating.data = post.rating
        form.title.data = post.title
        if post.uploads:
            form.picture.data = post.uploads
            app.logger.warning(post.uploads)
    return render_template('users/update_post.html',title='Update Post',form=form,form_legend="Update Post",post=post)

@users.route('/user/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.datePosted.desc())\
        .paginate(page=page,per_page=8)
    return render_template('user_posts.html',posts=posts,user=user)
