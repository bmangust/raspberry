import requests, json
import time, sys
import RPi.GPIO as G
from flask import Flask, send_file
from flask_socketio import SocketIO

#def init():
app = Flask('feedback')
socketio = SocketIO(app)

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

url = "http://api.openweathermap.org/data/2.5/forecast"
payload = {
    "lat": "55.751244",
    "lon": "37.618423",
    "units": "metric",
    "appid": "04dc5d24c41399f1965d3362d531c1d0",
}


@socketio.on('isPressed')
def checkButton(recievedData):
    data = {btn : G.input(btn) for btn in btns}
    socketio.emit('button', data)
    if G.input(btns[0]) == False:
        G.cleanup()
        sys.exit()
    elif data.get('3') == False:
        lights(False)
    else:
        lights(True)


def lights(btn):
    print('lights')
    delay=0.2
    while (btn == False):
        for i in range(2):
            time.sleep(delay)
            G.output(bleds[i], G.HIGH)
        for i in range(2):
            time.sleep(delay)
            G.output(bleds[i], G.LOW)
    for i in range(2):
        time.sleep(delay)
        G.output(bleds[i], G.LOW)


def pars_weather(weatherType, timeRange, measurementUnits):
    if (weatherType in weather) and (
        timeRange in weather[weatherType].keys()
    ):
        print(
            weatherType,
            ": ",
            weather[weatherType][timeRange],
            measurementUnits,
        )
    else:
        print(weatherType, ": ", "none")


def display_temp(temp):
    if (temp < 0):
       G.output(bleds[0], G.HIGH)
    elif temp >= 0 and temp < 3:
       G.output(bleds[0], G.HIGH)
       G.output(bleds[1], G.HIGH)
    else:
       G.output(bleds[0], G.HIGH)
       G.output(bleds[1], G.HIGH)
       G.output(bleds[2], G.HIGH)

#def main():
#init()

res = requests.get(url, params=payload)
data = json.loads(res.text)

weather = data['list'][0]

socketio.run(app, port=3000, host='0.0.0.0')

temp = weather["main"]["temp"] 
pars_weather("clouds", "all", "%")
pars_weather("rain", "3h", "mm")
pars_weather("snow", "3h", "mm")
print("temp:", temp, "C")
display_temp(temp)

#if __name__ == '__main__':
#    main
