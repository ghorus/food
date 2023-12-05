from flask import Blueprint,flash,redirect,render_template,request,url_for
from flask_login import current_user
from foodInnerFolder import db
from foodInnerFolder.models import Post,User

main = Blueprint('main',__name__)

@main.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(page=page,per_page=2)
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
