from flask import Flask, send_file
import RPi.GPIO as G

G.setmode(G.BCM)
led = 18
G.setup(led, G.OUT)

app = Flask('lightControl')

@app.route('/')
def index():
    return send_file('light.html')

@app.route('/images/<filename>')
def get_image(filename):
    return send_file('images/'+filename)


"""
@app.route('/turnOn')
def turnOn():
    G.output(led, G.HIGH)
    return 'turnedOn'

@app.route('/turnOff')
def turnOff():
    G.output(led, G.LOW)
    return 'turnedOff'
"""

@app.route('/<state>')
def turn(state):
    if (state == 'turnOn'):
        G.output(led, G.HIGH)
    elif (state == 'turnOff'):
        G.output(led, G.LOW)
    return 'done'




app.run(debug=True, port=3000, host='0.0.0.0')
