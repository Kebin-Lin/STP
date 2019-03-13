from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request
from util import Game
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app)

rooms = {}
names = {}
games = {}

@app.route("/")
def root():
    return render_template("index.html")

@socketio.on("joinRoom")
def joinRoom(roomInfo):
    if len(roomInfo) == 0:
        return
    if request.sid in rooms: #Checks if the user is already in a room
        if rooms[request.sid] == roomInfo:
            return
        leave_room(rooms[request.sid])
        send("<b> " + names[request.sid] + " has left the room<b>", room=rooms[request.sid])
        winner = Game.removeUser(games[rooms[request.sid]], request.sid)
        if len(games[rooms[request.sid]]['users']) == 0: #Deletes game room if no-one is in it
            games.pop(rooms[request.sid])
        elif winner != None:
            send("<b>" + names[games[rooms[request.sid]][winner]] + " has won the game!</b>", room = rooms[request.sid])
    join_room(roomInfo) #Places user in a room
    if roomInfo not in games: #Create new game
        games[roomInfo] = Game.newGame()
    Game.addUser(games[roomInfo],request.sid)
    rooms[request.sid] = roomInfo #Sets room of user in a dictionary for later use
    emit('joinRoom', roomInfo)
    emit('gameUpdate', games[roomInfo]['board'])
    send("<b> " + names[request.sid] + " joined " + roomInfo + "<b>", room=roomInfo)

@socketio.on('setName')
def setname(name):
    if len(name) == 0: #Default name
        name = "CoolBean"
    names[request.sid] = name

@socketio.on('disconnect')
def disconn(): #Executed when a client disconnects from the server
    try:
        send("<b> " + names[request.sid] + " has left the room<b>", room=rooms[request.sid])
        winner = Game.removeUser(games[rooms[request.sid]], request.sid)
        if len(games[rooms[request.sid]]['users']) == 0: #Deletes game room if no-one is in it
            games.pop(rooms[request.sid])
        elif winner != None:
            send("<b>" + names[games[rooms[request.sid]][winner]] + " has won the game!</b>", room = rooms[request.sid])
        rooms.pop(request.sid)
    except: #Fallback in case user leaves before joining a room
        pass
    names.pop(request.sid)

@socketio.on('makeMove')
def makeMove(move):
    currGame = games[rooms[request.sid]]
    if currGame['end']: #Executes if the game is already over
        currGame['board'] = '         '
        currGame['end'] = False
        emit('gameUpdate', currGame['board'], room=rooms[request.sid])
        return
    countx = currGame['board'].count('x')
    counto = currGame['board'].count('o')
    mover = 'x' if countx == counto else 'o'
    if currGame[mover] != request.sid:
        return
    Game.makeMove(currGame, int(move[-1]) % 9, mover)
    outcome = Game.checkStatus(currGame)
    emit('gameUpdate', currGame['board'], room=rooms[request.sid])
    if outcome != None:
        if outcome == "Draw":
            send("<b>This game has resulted in a draw</b>", room = rooms[request.sid])
        else:
            send("<b>" + names[currGame[outcome]] + " has won the game!</b>", room = rooms[request.sid])
        currGame['end'] = True

@socketio.on('message')
def message(msg):
    if len(msg) != 0:
        send("<b>" + names[request.sid] + ": </b>" + msg, room = rooms[request.sid])

if __name__ == '__main__':
    socketio.run(app, debug = True)
