from flask import Flask, send_file
from flask_socketio import SocketIO
import time
import RPi.GPIO as G

G.setmode(G.BCM)
btns = [2,3,4,8]
leds = [10,12,13,14,15,16,17,18,19,21,24,26]
for btn in btns:
    G.setup(btn, G.IN)
for led in leds:
    G.setup(led, G.OUT)

app = Flask('feedback')
socketio = SocketIO(app)

@app.route('/')
def index():
	return send_file('feedback.html')

@app.route('/images/<filename>')
def get_image(filename):
	return send_file('images/'+filename)

@socketio.on('isPressed')
def checkButton(recievedData):
    data = {btn : G.input(btn) for btn in btns}
    socketio.emit('button', data)
    if G.input(btns[0]) == False:
        raise KeyboardInterrupt
    elif data.get('3') == False:
        lights(False)
    else:
        lights(True)

def lights(btn):
    print('lights')
    delay=0.2
    while (btn == False):
        for i in [2,8,5]:
            time.sleep(delay)
            G.output(leds[i], G.HIGH)
        for i in [2,8,5]:
            time.sleep(delay)
            G.output(leds[i], G.LOW)
    for i in [2,8,5]:
        time.sleep(delay)
        G.output(leds[i], G.LOW)

try:
	socketio.run(app, port=3000, host='0.0.0.0')
except KeyboardInterrupt:
	print('exiting')
finally:
	G.cleanup()  


"""
@app.route('/turnOn')
def turnOn():
    G.output(led, G.HIGH)
    return 'turnedOn'

@app.route('/turnOff')
def turnOff():
    G.output(led, G.LOW)
    return 'turnedOff'


@app.route('/<state>')
def turn(state):
    if (state == 'turnOn'):
        G.output(led, G.HIGH)
    elif (state == 'turnOff'):
        G.output(led, G.LOW)
    return 'done'

"""
