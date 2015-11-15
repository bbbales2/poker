import flask
import os
import sys
import socket

bufferSize = 1024

appDir = os.path.abspath(os.path.dirname(__file__))

app = flask.Flask('poker', template_folder = appDir + '/templates/')

states = []
actions = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1.0)
s.connect(('127.0.0.1', int(sys.argv[1])))
s.send('VERSION:2:0:0\r\n')
#s.close()
print "listening to socket!"

@app.route('/play')
def play():
    action = flask.request.args.get('action', None)

    if action in 'fcr':
        message = "{0}:{1}".format(states[-1] if len(states) > 0 else '', action)
        print "web ui writes: " + message
        s.send(message)

    return flask.json.jsonify({})

@app.route('/get_state')
def get_state():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(1.0)
        s.connect(('127.0.0.1', int(sys.argv[1])))
        data = s.recv(bufferSize)
        
        if len(data) > 0:
            print "web ui receives: " + data
            states.append(data)
    except socket.timeout:
        print "Socket timeout"
    finally:
        s.close()

    return flask.json.jsonify(state = states[-1] if len(states) > 0 else '')

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)

