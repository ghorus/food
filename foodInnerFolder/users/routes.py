from flask import abort,Blueprint,flash,redirect,render_template,request,url_for
from flask_login import login_user,login_required,logout_user,current_user
from flask_mail import Message
from foodInnerFolder import app, bcrypt, db, mail
from foodInnerFolder.models import Post,User 
from foodInnerFolder.users.forms import (LoginForm,PostForm,RegistrationForm,RequestResetForm,
                                         ResetPasswordForm,UpdateAccountForm)
import os
from PIL import Image
import secrets
from werkzeug.utils import secure_filename

users = Blueprint('users',__name__)

@users.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        # redirect instead of going to return render template to avoid another post request 
        # when reloading page
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('users/account.html',form=form,image_file=image_file, title='Account')

@users.route('/post/<post_id>/delete',methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
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
            flash("You've succesfully logged in",'success')
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password.','danger')
    return render_template('users/login.html',form=form,title='Login')

@users.route("/logout")
def logout():
    logout_user()
    flash("You've logged out.",'success')
    return redirect(url_for('main.home'))

@users.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = ""
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
        post = Post( author=current_user,city=form.city.data,content=form.content.data,name=form.name.data,picture=picture_file,rating=form.rating.data,title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created.",'success')
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

@users.route('/post/<post_id>/update',methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('users.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('users/update_post.html',title='Update Post',form=form,form_legend="Update Post")

@users.route('/user/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.datePosted.desc())\
        .paginate(page=page,per_page=8)
    return render_template('user_posts.html',posts=posts,user=user)

def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    print(picture_path)
    return picture_fn

def save_post_picture(form_picture):
    app.config['UPLOAD_FOLDER'] = 'static/post_pics'
    _, f_ext = os.path.splitext(form_picture.filename)
    random_hex = secrets.token_hex(8)
    picture_fn = secure_filename(random_hex + f_ext)
    picture_path = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],picture_fn)
    form_picture.save(picture_path)
    print(picture_path)
    return picture_fn

def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='nguyen.victor4@gmail.com',recipients=[user.email])
    msg.body = f'''
    To reset, please click on the following link:
    {url_for('users.reset_token',salt='something',token=token,_external=True)}
    If you didn't make this request, then you can simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
