#location features
import json
from urllib.request import urlopen
from geopy.geocoders import Nominatim
from geopy import distance
import geocoder
#flask
from flask import Blueprint,flash,redirect,render_template,request,send_file,url_for
from flask_login import current_user
from flask_socketio import emit, send
from foods import db,socketio,app
from foods.models import Food_Post_Upload,Post,Profile_Pic_Upload,User
from io import BytesIO
main = Blueprint('main',__name__)

@main.route("/get_loc")
def get_loc(locs):
    geolocator = Nominatim(user_agent="foodLocator")
    #current loc of user
    data = (geocoder.ip('me')).latlng
    curr_place = (data[0],data[1])
    #location of food spots
    location = []
    distances = []
    for loc in locs:
        location.append(loc.address)
    for loc in location:
        coord = geolocator.geocode(loc,timeout=5)
        if coord:
            lat,lon = (coord.latitude),(coord.longitude)
            place = (lat,lon)
            dist = round(distance.distance(curr_place,place).mi,1)
            distances.append(dist)
        else:
            distances.append(None)
    return distances

@main.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(page=page,per_page=5)
    usersTotal = len(User.query.all())
    return render_template('index.html',posts=posts,title="Home",users=usersTotal)

@socketio.on('like',namespace='/likes')
def like(post_id):
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

@main.route("/search")
def search():
    return render_template('search/search.html')

@main.route("/search_result")
def search_result():
    q = request.args.get('q')
    distances = None
    if q:
        results = Post.query.filter(Post.name.icontains(q) | Post.address.icontains(q)| Post.category.icontains(q) | Post.title.icontains(q)).all()
        distances = get_loc(results)
    else:
        results=[]
    return render_template('search/search_result.html',results=results,distances = distances)

@main.route("/upload_pic/<id>")
def upload(id):
    upload = Profile_Pic_Upload.query.filter_by(id=id).first()
    return send_file(BytesIO(upload.data),download_name = upload.filename,as_attachment=True)

@main.route("/upload_foodPic/<id>")
def uploadFood(id):
    upload = Food_Post_Upload.query.filter_by(id=id).first()
    return send_file(BytesIO(upload.data),download_name = upload.filename,as_attachment=True)
