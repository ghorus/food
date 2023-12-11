from flask import Blueprint,flash,redirect,render_template,request,send_file,url_for
from flask_login import current_user
from flask_socketio import emit, send
from foodInnerFolder import db,socketio,app
from foodInnerFolder.models import Food_Post_Upload,Post,Profile_Pic_Upload,User
from io import BytesIO

main = Blueprint('main',__name__)

@main.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',posts=posts,title="Home")

@main.route("/upload_pic/<id>")
def upload(id):
    upload = Profile_Pic_Upload.query.filter_by(id=id).first()
    return send_file(BytesIO(upload.data),download_name = upload.filename,as_attachment=True)

@main.route("/upload_foodPic/<id>")
def uploadFood(id):
    upload = Food_Post_Upload.query.filter_by(id=id).first()
    return send_file(BytesIO(upload.data),download_name = upload.filename,as_attachment=True)

@socketio.on('like')
def like(post_id):
    app.logger.warning('user just liked something')
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        post = Post.query.filter_by(id=post_id).first()
        if post in user.likes:
            user.likes.remove(post)
            db.session.commit()
            emit('like',len(post.liker))

        elif post not in user.likes:
            user.likes.append(post)
            db.session.add(user)
            db.session.commit()
            emit('like',len(post.liker))

    elif current_user.is_authenticated == False:
        emit('redirect', url_for('users.login'))

