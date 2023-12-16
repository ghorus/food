from flask import Blueprint,render_template,redirect,request,url_for
from flask_login import login_required,current_user
from flask_socketio import emit,join_room,leave_room,send
from foods import socketio,app,db
from foods.models import AdlibPost,Game_Room,Game_Room_Members,Game_Room_Messages,User
from foods.users.forms import CreateGameRoomForm,GameRoomMessageForm,JoinRoomForm
import random 
import string

game = Blueprint('game',__name__)

def room_id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#all adlib posts
@game.route("/adlibposts",methods=['GET','POST'])
def adlibposts():
    adlib_posts = AdlibPost.query.all()
    auths = User.query.all()
    return render_template("game/adlibposts.html",adlib_posts=adlib_posts,auths=auths)

@game.route("/creategameroom",methods=['GET','POST'])
@login_required
def creategameroom():
    form = CreateGameRoomForm()
    if form.validate_on_submit():
        room_link = room_id_generator()
        game_room = Game_Room(name = form.name.data,room_link=room_link,turn=0)
        creator = Game_Room_Members(member_id=current_user.id,room_id=room_link)
        db.session.add(game_room)
        db.session.commit()
        db.session.add(creator)
        db.session.commit()
        return redirect(url_for('game.gameroom',link=room_link))
    return render_template("game/creategameroom.html",form=form)

@game.route("/gameroom/<link>",methods=['GET','POST'])
@login_required
def gameroom(link):
    messageForm = GameRoomMessageForm()
    room_info = Game_Room.query.filter_by(room_link = link).first()
    members = Game_Room_Members.query.filter_by(room_id=link).all()
    messages = Game_Room_Messages.query.all()
    return render_template("game/gameroom.html",link=link,members=members,messages=messages, messageForm=messageForm,room_info=room_info)

@game.route("/joingameroom",methods=['GET','POST'])
@login_required
def joingameroom():
    joinForm = JoinRoomForm()
    gamerooms = Game_Room.query.all()
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
        return redirect(url_for('game.gameroom',link=joinForm.room.data))
    return render_template("game/joinroom.html",gamerooms=gamerooms,joinForm=joinForm)

@socketio.on("post adlib",namespace='/posting')
def postAdlib(data):
    adlib = AdlibPost(authors=data['members'],content=data['adlibs'],title=data['roomTitle'])
    db.session.add(adlib)
    db.session.commit()
    #delete all info from that room:room,members,&messages
    room = Game_Room.query.filter_by(room_link=data['room_link']).first()
    if room:
        db.session.delete(room)
        db.session.commit()
    room_members = Game_Room_Members.query.filter_by(room_id=data['room_link']).all()
    room_messages = Game_Room_Messages.query.filter_by(room_id=data['room_link']).all()
    if room_members:
        for member in room_members:
            db.session.delete(member)
            db.session.commit()
    if room_messages:
        for message in room_messages:
            db.session.delete(message)
            db.session.commit()
    emit('redirect', url_for('game.adlibposts'))

#create adlib message in game room
@socketio.on("send game message",namespace='/messaging')
def sendGameMessage(data):
    user_is_member = False
    members = Game_Room_Members.query.filter_by(room_id=data['link']).all()
    ms = []
    for member in members:
        ms.append(member.member_id)
        if current_user.id == member.member_id:
            user_is_member = True
    #if spectators are watching, then they can't participate and mess with people in the room,
    if user_is_member == True:
        room = Game_Room.query.filter_by(room_link=data['link']).first()
        room_turn = room.turn
        current_member_turn = User.query.filter_by(id=ms[room_turn]).first()
        #if not their turn, flash message
        if ms[room_turn] != current_user.id:
            emit('flashy',f"It\'s {current_member_turn.username}\'s turn!")
        #if it is the member's turn, then do this
        elif ms[room_turn] == current_user.id:    
            if " " in data['message']:
                emit('flashy',"Please submit only 1 word. Make sure there's no spaces.")
            elif data['message']=="":
                emit('flashy',"Please submit something to the adlib!")
            elif " " not in data['message']:
                message = Game_Room_Messages(member_id=current_user.id,room_id=data['link'],member_message=data['message'])
                db.session.add(message)
                db.session.commit()
                #if its the last in the list, go back to index 0, otherwise keep going
                if room.turn + 1 > (len(ms)-1):
                    room.turn = 0
                    db.session.commit()
                elif room.turn + 1 <= (len(ms)-1):
                    room.turn += 1
                    db.session.commit()
    else:
        emit('redirect', url_for('game.joingameroom'))
    messages = Game_Room_Messages.query.all()
    msgs= []
    for message in messages:
        if message.room_id == data['link']:
            msgs.append(message.member_message)
    emit('send game message',msgs,room=data['link'])

@socketio.on("join",namespace='/messaging')
def join(data):
    join_room(data['roomLink'])
    members = Game_Room_Members.query.filter_by(room_id=data['roomLink']).all()
    members_usernames = []
    for member in members:
        user = User.query.filter_by(id=member.member_id).first()
        members_usernames.append(user.username)
    emit('members',members_usernames,room=data['roomLink'])

@socketio.on('dc',namespace='/messaging')
def on_leave(data):
    room_members = Game_Room_Members.query.filter_by(room_id=data).all()
    emit('flashy','someone left',broadcast=True)
    for member in room_members:
        if member.member_id == current_user.id:
            db.session.delete(member)
            db.session.commit()


