from flask import Flask
from flask import jsonify
from flask import make_response
from flask_socketio import SocketIO
from scapy.all import *
import requests
# conf.verb = 0 // this is a scapy thing, not sure what it is

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/payload')
def hello_world():
    p = IP(dst="github.com")/TCP()
    r = sr1(p)
    resp = make_response(jsonify(r.summary()))
    # required to work with p5 web editor
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@socketio.on('connected')
def handle_message(message):
    print('Received message: ' + message['data'])

if __name__ == '__main__':
    socketio.run(app)
