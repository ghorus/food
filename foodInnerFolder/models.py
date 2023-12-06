from datetime import datetime
from flask_login import UserMixin
from foodInnerFolder import app,db,login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer

#loads the current user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_post = db.Table('user_post',
    # db.Column( db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

# class User_Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
#     post = db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
#     def __repr__(self):
#         return f"User('{self.user}','{self.post}')"

class User(db.Model, UserMixin):
    email = db.Column(db.String(120),unique=True,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    likes = db.relationship('Post', secondary=user_post, backref='liker')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post',backref='author',lazy=True)
    uploads = db.relationship('Upload',backref='pic_owner',lazy=True)
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
        return f"User('{self.username},'{self.email}','{self.password},'{self.image_file})"
    
class Post(db.Model, UserMixin):
    content = db.Column(db.String(2000),nullable=False)
    city = db.Column(db.String(200),nullable=False)
    datePosted = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    rating = db.Column(db.Integer,nullable=False)
    title = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"User('{self.title},'{self.datePosted}','{self.id})"

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)