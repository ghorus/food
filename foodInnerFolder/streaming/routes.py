from flask import Blueprint,render_template,request,session,redirect,url_for
from flask_socketio import leave_room, join_room,send
from foodInnerFolder import socketio,app
import random
from string import ascii_uppercase

stream = Blueprint('stream',__name__)
rooms = {}
def gen_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code+=random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@stream.route("/createroom",methods=["GET","POST"])
def createroom():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        create = request.form.get("create",False)
        join = request.form.get("join",False)
        if not name:
            return render_template("streaming/createroom.html",error="Please input a name",code=code,name=name)
        if join !=False and not code:
            return render_template("streaming/createroom.html",error="Please put a code.",code=code,name=name)
        room = code
        if create != False:
            room = gen_unique_code(4)
            rooms[room] = {"members":0,"messages":[]}
        elif code not in rooms:
            return render_template("streaming/createroom.html",error="this room doesn't exist")
        session["room"]=room
        session["name"]=name
        return redirect(url_for("stream.room"))
    return render_template("streaming/createroom.html")

@stream.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("stream.createroom"))
    return render_template("streaming/room.html",room=room,messages=rooms[room]["messages"])

#sockets
@socketio.on("connect")
def connect():
    name = session.get("name")
    room = session.get("room")
    if not room or not name:
        return 
    if room not in rooms:
        leave_room(room)
        return 
    join_room(room)
    send({"name":name,"message":"has entered the room"},to=room)
    rooms[room]["members"]+=1

@socketio.on("disconnect")
def disconnect():
    name = session.get("name")
    room = session.get("room")
    if room in rooms:
        rooms[room]["members"]-=1
        if rooms[room]["members"]<=0:
            del rooms[room]
    send({"name":name,"message":"has left the room"},to=room)

@socketio.on("message")
def handle_msgs(data):
    room = session.get("room")
    if room not in rooms:
        return
    content ={"name":session.get("name"),
              "message":data["data"]}
    send(content,to=room)
    rooms[room]["messages"].append(content)
    return render_template("streaming/room.html",)