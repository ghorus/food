from datetime import datetime
from flask_login import UserMixin
from foodInnerFolder import app,db,login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
import secrets

#loads the current user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    email = db.Column(db.String(120),unique=True,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(40), nullable = False)
    username = db.Column(db.String(20),unique=True,nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id},salt='something')
    
    @staticmethod
    def verify_reset_token(token,expires_sec=20):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,salt='something',max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username},'{self.email}','{self.password},'{self.image_file})"
    
class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    content = db.Column(db.String(2000),nullable=False)
    datePosted = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"User('{self.title},'{self.datePosted}','{self.id})"
