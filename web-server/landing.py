from flask import Flask, send_file
from flask_socketio import SocketIO
import time
import RPi.GPIO as G

G.setmode(G.BCM)
btns = [2,3,4,8]
bleds = [10,12,14,15,17,18,21,24,26]
oleds = [13, 19, 16]
for btn in btns:
    G.setup(btn, G.IN)
for led in bleds:
    G.setup(led, G.OUT)
for led in oleds:
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
    delay=0.2
    data = {btn : G.input(btn) for btn in btns}
    socketio.emit('button', data)
    print(data)
    if G.input(btns[1]) == False:
        G.output(bleds[0], G.HIGH)
        print('butt 0 is pressed')
    elif G.input(btns[0]) == False:
        for led in oleds:
            time.sleep(delay)
            G.output(led, G.HIGH)
        for led in oleds:
            time.sleep(delay)
            G.output(led, G.LOW)
    else:
        for led in bleds:
            time.sleep(delay)
            G.output(led, G.LOW)
        for led in oleds:
            time.sleep(delay)
            G.output(led, G.LOW)

def main():
    try:
        socketio.run(app, port=3000, host='0.0.0.0')
    #except KeyboardInterrupt:
    #	print('exiting')
    finally:
        print('finally')
        G.cleanup()  

if __name__ == '__main__':
    main()
    #G.cleanup()
