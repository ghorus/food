from flask import Flask


app = Flask(__name__)

from foodInnerFolder.foodReviews.routes import foodReviewz
from foodInnerFolder.main.routes import main

app.register_blueprint(foodReviewz)
app.register_blueprint(main)
