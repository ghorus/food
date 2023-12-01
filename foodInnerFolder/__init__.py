from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SECRET_KEY'] = os.environ.get('foodSecretKey')
db = SQLAlchemy(app)

from foodInnerFolder.foodReviews.routes import foodReviewz
from foodInnerFolder.main.routes import main
from foodInnerFolder.users.routes import users

app.register_blueprint(foodReviewz)
app.register_blueprint(main)
app.register_blueprint(users)

