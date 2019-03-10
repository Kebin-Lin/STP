from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request
from util import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app)

rooms = {}

@app.route("/")
def root():
    return render_template("index.html")

@socketio.on("joinRoom",'/')
def joinRoom(roomInfo):
    if request.sid in rooms:
        leave_room(rooms[request.sid])
    join_room(roomInfo)
    rooms[request.sid] = roomInfo
    emit('joinRoom', roomInfo)

@socketio.on('message')
def message(msg):
    send(msg, room = rooms[request.sid], broadcast = True)

if __name__ == '__main__':
    socketio.run(app, debug = True)
