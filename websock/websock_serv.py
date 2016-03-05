from flask import Flask, render_template
from flask.ext.socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('value changed')
def value_changed(message):
    print(message)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
