from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request
from util import Game
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
socketio = SocketIO(app)

@app.route("/")
def root():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app, debug = True)
