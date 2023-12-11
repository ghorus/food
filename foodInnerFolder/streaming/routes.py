from flask import Blueprint,render_template,request,session,redirect,url_for
from flask_socketio import emit
from foodInnerFolder import socketio,app


stream = Blueprint('stream',__name__)

@stream.route("/streaming/<int:host>")
def streaming(host):
    return render_template("streaming/stream.html",host = host)

@socketio.on("listen to new users")
def new_user_connected(user_id):
    emit('listen to new users',user_id,broadcast=True)

@socketio.on("user dc")
def user_disconnected(user_id):
    emit('user dc',user_id)