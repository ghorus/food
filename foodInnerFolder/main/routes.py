import base64
from flask import Blueprint,flash,redirect,render_template,request,send_file,url_for
from flask_login import current_user
from foodInnerFolder import db
from foodInnerFolder.models import Post,Upload,User
from io import BytesIO

main = Blueprint('main',__name__)

@main.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(page=page,per_page=2)
    return render_template('index.html',posts=posts,title="Home")


@main.route("/testUpload",methods=['GET','POST'])
def test_upload():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename=file.filename,data=file.read())
        db.session.add(upload)
        db.session.commit()
    return render_template('testUpload.html',title="testUpload")

@main.route("/dl/<id>")
def download(id):
    upload = Upload.query.filter_by(id=id).first()
    return send_file(BytesIO(upload.data),download_name = upload.filename,as_attachment=True)

@main.route("/dl")
def pics():
    pics = Upload.query.all()
    return render_template('pics.html',pics=pics,title="testPics")

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
