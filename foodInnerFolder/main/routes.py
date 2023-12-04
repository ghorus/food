from flask import Blueprint, render_template,request
from foodInnerFolder.models import Post

main = Blueprint('main',__name__)

@main.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(page=page,per_page=2)
    return render_template('index.html',posts=posts,title="Home")
