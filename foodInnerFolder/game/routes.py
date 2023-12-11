from flask import Blueprint,render_template,redirect,url_for
from flask_login import login_required,current_user
from flask_socketio import emit
from foodInnerFolder import socketio,app,db
from foodInnerFolder.models import Game_Room
from foodInnerFolder.users.forms import CreateGameRoomForm


game = Blueprint('game',__name__)

@game.route("/gamerooms",methods=['GET','POST'])
@login_required
def gamerooms():
    form = CreateGameRoomForm()
    gamerooms = Game_Room.query.all()
    if form.validate_on_submit():
        game_room = Game_Room(name = form.name.data,host_id=current_user.id)
        db.session.add(game_room)
        db.session.commit()
        return redirect(url_for('game.gameroom',host_id = current_user.id))
    return render_template("game/gamerooms.html",form=form,gamerooms=gamerooms)

@game.route("/gameroom/<host_id>")
@login_required
def gameroom(host_id):
    return render_template("game/gameroom.html",host_id=host_id)

@socketio.on("create a game")
def new_user_connected():
    emit('create a game','hi')

# @socketio.on("game it")
# def streamit(data):
#     app.logger.warning(data)
#     emit('stream it',data)