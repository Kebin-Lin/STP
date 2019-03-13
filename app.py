from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request
from util import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app)

rooms = {}
names = {}

@app.route("/")
def root():
    return render_template("index.html")

@socketio.on("joinRoom",'/')
def joinRoom(roomInfo):
    if len(roomInfo) == 0:
        return
    if request.sid in rooms: #Checks if the user is already in a room
        if rooms[request.sid] == roomInfo:
            return
        leave_room(rooms[request.sid])
    join_room(roomInfo) #Places user in a room
    rooms[request.sid] = roomInfo #Sets room of user in a dictionary for later use
    emit('joinRoom', roomInfo)
    send("<b> " + names[request.sid] + " joined " + roomInfo + "<b>", room=roomInfo)

@socketio.on('setName')
def setname(name):
    if len(name) == 0: #Default name
        name = "CoolBean"
    names[request.sid] = name

@socketio.on('message')
def message(msg):
    if len(msg) != 0:
        send("<b>" + names[request.sid] + ": </b>" + msg, room = rooms[request.sid])

if __name__ == '__main__':
    socketio.run(app, debug = True)
