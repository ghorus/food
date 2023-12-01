from datetime import datetime
from flask_login import UserMixin
from foodInnerFolder import db

class User(db.Model, UserMixin):
    email = db.Column(db.String(120),unique=True,nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(60), nullable = False)
    username = db.Column(db.String(20),unique=True,nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username},'{self.email}','{self.password},'{self.image_file})"
    
class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    datePosted = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"User('{self.title},'{self.datePosted}','{self.id})"
