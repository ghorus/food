from datetime import datetime
from flask_login import UserMixin
from foods import app,db,login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer

#loads the current user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Food_Post_Upload(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),nullable=False)

class Game_Room(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable=False)
    room_link = db.Column(db.String(4),nullable=False)

class Game_Room_Members(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    room_id = db.Column(db.String(4),nullable=False)

class Game_Room_Messages(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    member_message = db.Column(db.String(50),nullable=False)
    room_id = db.Column(db.String(4),nullable=False)

class Post(db.Model, UserMixin):
    content = db.Column(db.String(2000),nullable=False)
    city = db.Column(db.String(200),nullable=False)
    datePosted = db.Column(db.DateTime,default=datetime.now(),nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    uploads = db.relationship('Food_Post_Upload',backref='belongs_to_post',lazy=True)
    rating = db.Column(db.Integer,nullable=False)
    title = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"User('{self.title},'{self.datePosted}','{self.id})"

class Profile_Pic_Upload(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

user_post = db.Table('user_post',
    # db.Column( db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

class User(db.Model, UserMixin):
    email = db.Column(db.String(120),unique=True,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    likes = db.relationship('Post', secondary=user_post, backref='liker')
    member = db.relationship('Game_Room_Members',backref='member',lazy=True)
    messages = db.relationship('Game_Room_Messages',backref='author',lazy=True)
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post',backref='author',lazy=True)
    uploads = db.relationship('Profile_Pic_Upload',backref='pic_owner',lazy=True)
    username = db.Column(db.String(20),unique=True,nullable=False)

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id},salt='something')
    
    @staticmethod
    def verify_reset_token(token,expires_sec=100):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,salt='something',max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username},'{self.email}','{self.password},'{self.uploads})"
    