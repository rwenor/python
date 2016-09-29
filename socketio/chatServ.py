import socketio
import eventlet
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)

@app.route('/')
def index():
    # """Serve the client-side application."""
    return render_template('chat.html')

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('chat message')
def message(sid, data):
    print('message ', data)
    emit('chat message', message, broadcast=True)

@sio.on('my event')
def message(sid, data):
    print('event: ', data)
    
@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
