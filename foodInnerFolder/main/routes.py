from flask import Blueprint, render_template
from foodInnerFolder.models import User

main = Blueprint('main',__name__)

@main.route("/")
def home():
    users = User.query.all()
    return render_template('index.html',users = users,title="Home")
