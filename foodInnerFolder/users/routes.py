from flask import Blueprint,flash,redirect,render_template,request,url_for
from flask_login import login_user,login_required,logout_user,current_user
from foodInnerFolder import app, bcrypt, db
from foodInnerFolder.models import User 
from foodInnerFolder.users.forms import LoginForm,RegistrationForm,UpdateAccountForm
import os
from PIL import Image
import secrets

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
    return redirect(url_for('main.home'))

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

def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn