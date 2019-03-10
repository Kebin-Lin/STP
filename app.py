from flask_socketio import SocketIO, join_room, emit, send
from flask import Flask, render_template
from util import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app)

rooms = {}

@app.route("/")
def root():
    return render_template("index.html")

@socketio.on("createRoom",'/')
def createRoom(roomInfo):
    print("Recieved Room Creation Info: " + str(roomInfo))
    roomID = 'someRoom'
    join_room(roomID)
    rooms[roomID] = roomInfo
    emit('joinRoom', roomID)

@socketio.on('joinRoom')
def joinRoom(joinInfo):
    roomID = joinInfo['roomID']
    if roomID in rooms:
        print(1)
    else:
        emit('error','Room does not exist.')

@socketio.on('message')
def message(msg):
    send('Hi to everyone in someRoom', room = 'someRoom', broadcast = True)

if __name__ == '__main__':
    socketio.run(app, debug = True)
