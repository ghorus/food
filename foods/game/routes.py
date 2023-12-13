from flask import Blueprint,flash,render_template,redirect,request,url_for
from flask_login import login_required,current_user
from flask_socketio import emit
from foods import socketio,app,db
from foods.models import Game_Room,Game_Room_Members
from foods.users.forms import CreateGameRoomForm,JoinRoomForm
import random 
import string

game = Blueprint('game',__name__)

def room_id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@game.route("/gamerooms",methods=['GET','POST'])
@login_required
def gamerooms():
    form = CreateGameRoomForm()
    joinForm = JoinRoomForm()
    gamerooms = Game_Room.query.all()
    if form.validate_on_submit():
        room_link = room_id_generator()
        app.logger.warning(type(room_link))
        game_room = Game_Room(name = form.name.data,room_link=room_link)
        creator = Game_Room_Members(member_id=current_user.id,room_id=room_link)
        db.session.add(game_room)
        db.session.commit()
        db.session.add(creator)
        db.session.commit()
        return redirect(url_for('game.gameroom',link=room_link))
    if joinForm.validate_on_submit():
        members = Game_Room_Members.query.filter_by(room_id=joinForm.room.data).all()
        newMember = None
        for member in members:
            if member.member_id == current_user.id:
                newMember = member.member_id
        if not newMember:
            newMember = Game_Room_Members(member_id=current_user.id,room_id=joinForm.room.data)
            db.session.add(newMember)
            db.session.commit()


    return render_template("game/gamerooms.html",form=form,gamerooms=gamerooms,joinForm=joinForm)

@game.route("/gameroom/<link>",methods=['GET','POST'])
@login_required
def gameroom(link):
    # form = GameRoomMessagesForm()
    # gameroom = Game_Room.query.filter_by(host_id=host_id).first()
    # if str(current_user.id)not in members.split(","):
    #     flash('Either the room is full or you haven\'t joined this room yet!','info')
    #     return redirect(url_for('game.gamerooms'))
    # elif str(current_user.id) in members.split(","):
    #     pass
    # if form.validate_on_submit():
    #     if not gameroom.messages:
    #         pass
    #     else:
    #         gameroom.messages = gameroom.messages + "," + form.message.data
    #         db.session.commit()
    #         return redirect(url_for('game.gameroom',host_id=gameroom.host_id,members = gameroom.members))

    return render_template("game/gameroom.html")

# @socketio.on("create a game")
# def new_user_connected():
#     emit('create a game','hi')

# @socketio.on("game it")
# def streamit(data):
#     app.logger.warning(data)
#     emit('stream it',data)