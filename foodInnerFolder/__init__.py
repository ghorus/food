from flask import Flask
import os 

app = Flask(__name__)

from foodInnerFolder.foodReviews.routes import foodReviewz
from foodInnerFolder.main.routes import main
from foodInnerFolder.users.routes import users
d = os.environ.get('foodSecretKey')

app.register_blueprint(foodReviewz)
app.register_blueprint(main)
app.register_blueprint(users)

