from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
#for hashing password and protect
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
#in order to view
login_manager.login_view = 'users.login'
login_manager.login_message_category = "info"

from foodInnerFolder.foodReviews.routes import foodReviewz
from foodInnerFolder.main.routes import main
from foodInnerFolder.users.routes import users

app.register_blueprint(foodReviewz)
app.register_blueprint(main)
app.register_blueprint(users)

