from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.elasticemail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nguyen.victor4@gmail.com'
app.config['MAIL_PASSWORD'] = 'CED7D2CCE58243B1B8012FECDEDB519C464C'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SECRET_KEY'] = 'SECRET_KEY'
#for hashing password and protect
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
socketio = SocketIO(app)
login_manager = LoginManager(app)
#in order to view
login_manager.login_view = 'users.login'
login_manager.login_message_category = "info"
mail = Mail(app)

from foodInnerFolder.foodReviews.routes import foodReviewz
from foodInnerFolder.main.routes import main
from foodInnerFolder.streaming.routes import stream
from foodInnerFolder.users.routes import users

app.register_blueprint(foodReviewz)
app.register_blueprint(main)
app.register_blueprint(stream)
app.register_blueprint(users)

