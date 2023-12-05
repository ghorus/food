from flask import Blueprint,flash,redirect,render_template,request,url_for
from flask_login import current_user
from foodInnerFolder import app,db
from foodInnerFolder.models import Post,User
import os

main = Blueprint('main',__name__)

@main.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(page=page,per_page=2)
    app.logger.warning("#1" + os.path.abspath(__file__) + " something "+ app.root_path + ' #2 ')
    for post in post:
        picture_path = os.path.join(app.root_path, 'static/profile_pics',post.picture)
        app.logger.warning(post.picture + " 2 "+ picture_path)
    return render_template('index.html',posts=posts,title="Home")

@main.route("/<post_id>",methods=['POST'])
def like(post_id):
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        post = Post.query.filter_by(id=post_id).first()
    elif current_user.is_authenticated == False:
        flash('Must sign in to interact with post.','info')
        return redirect(url_for('users.login'))
    if post in user.likes:
        user.likes.remove(post)
        db.session.commit()
    elif post not in user.likes:
        user.likes.append(post)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('main.home'))
