from flask import Blueprint,flash,redirect,render_template,url_for
from foodInnerFolder.users.forms import LoginForm,RegistrationForm
users = Blueprint('users',__name__)

@users.route("/login",methods=['GET', 'POST'])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     flash("You've succesfully logged in",'success')
    #     return redirect(url_for('main.home'))
    return render_template('users/login.html',title='Login')

@users.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html',title='Register',form=form)