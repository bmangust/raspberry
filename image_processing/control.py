import RPi.GPIO as GPIO
import time
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)
buttons = [20, 21, 14, 6]
#control_pins = [13,19,26]
#26 SH_CP   clockPin
#19 DS      dataPin
#13 ST_CP   latchPin
clockPin = 26
dataPin = 13
latchPin = 19

GPIO.setup(clockPin, GPIO.OUT)
GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT)

for button in buttons:
    GPIO.setup(button, GPIO.IN)
    
halfstep_fw_1 = [
  [1,0,0,0,0,0,0,0],
  [1,1,0,0,0,0,0,0],
  [0,1,0,0,0,0,0,0],
  [0,1,1,0,0,0,0,0],
  [0,0,1,0,0,0,0,0],
  [0,0,1,1,0,0,0,0],
  [0,0,0,1,0,0,0,0],
  [1,0,0,1,0,0,0,0]
]
halfstep_bw_1 = [
  [0,0,0,1,0,0,0,0],
  [0,0,1,1,0,0,0,0],
  [0,0,1,0,0,0,0,0],
  [0,1,1,0,0,0,0,0],
  [0,1,0,0,0,0,0,0],
  [1,1,0,0,0,0,0,0],
  [1,0,0,0,0,0,0,0],
  [1,0,0,1,0,0,0,0]
]
halfstep_fw_2 = [
  [0,0,0,0,1,0,0,0],
  [0,0,0,0,1,1,0,0],
  [0,0,0,0,0,1,0,0],
  [0,0,0,0,0,1,1,0],
  [0,0,0,0,0,0,1,0],
  [0,0,0,0,0,0,1,1],
  [0,0,0,0,0,0,0,1],
  [0,0,0,0,1,0,0,1]
]
halfstep_bw_2 = [
  [0,0,0,0,0,0,0,1],
  [0,0,0,0,0,0,1,1],
  [0,0,0,0,0,0,1,0],
  [0,0,0,0,0,1,1,0],
  [0,0,0,0,0,1,0,0],
  [0,0,0,0,1,1,0,0],
  [0,0,0,0,1,0,0,0],
  [0,0,0,0,1,0,0,1]
]
halfstep_fw = [
  [1,0,0,0,1,0,0,0],
  [1,1,0,0,1,1,0,0],
  [0,1,0,0,0,1,0,0],
  [0,1,1,0,0,1,1,0],
  [0,0,1,0,0,0,1,0],
  [0,0,1,1,0,0,1,1],
  [0,0,0,1,0,0,0,1],
  [1,0,0,1,1,0,0,1]
]

fullstep_fw_1 = [
  [1,0,0,0,0,0,0,0],
  [0,1,0,0,0,0,0,0],
  [0,0,1,0,0,0,0,0],
  [0,0,0,1,0,0,0,0]
]
fullstep_bw_1 = [
  [0,0,0,1,0,0,0,0],
  [0,0,1,0,0,0,0,0],
  [0,1,0,0,0,0,0,0],
  [1,0,0,0,0,0,0,0]
]
fullstep_fw_2 = [
  [0,0,0,0,1,0,0,0],
  [0,0,0,0,0,1,0,0],
  [0,0,0,0,0,0,1,0],
  [0,0,0,0,0,0,0,1]
]
fullstep_bw_2 = [
  [0,0,0,0,0,0,0,1],
  [0,0,0,0,0,0,1,0],
  [0,0,0,0,0,1,0,0],
  [0,0,0,0,1,0,0,0]
]
fullstep_fw = [
  [1,0,0,0,1,0,0,0],
  [0,1,0,0,0,1,0,0],
  [0,0,1,0,0,0,1,0],
  [0,0,0,1,0,0,0,1]
]
fullstep_bw = [
  [0,0,0,1,0,0,0,1],
  [0,0,1,0,0,0,1,0],
  [0,1,0,0,0,1,0,0],
  [1,0,0,0,1,0,0,0]
]

idle = [0,0,0,0,0,0,0,0]

motor_commands = {
    'forward1': fullstep_fw_1,
    'backward1': fullstep_bw_1,
    'forward2': fullstep_fw_2,
    'backward2': fullstep_bw_2,
    'forward': fullstep_fw,
    'backward': fullstep_bw}

camera = PiCamera()


def pulsePin(pin):
    GPIO.output(pin, 1)
    time.sleep(0.0001)
    GPIO.output(pin, 0)
    

def outputCommand(cmd):
    for bit in cmd:
        GPIO.output(dataPin, bit)
        pulsePin(clockPin)
        time.sleep(0.00001)
    pulsePin(latchPin)


def rotate(selector):
    cnt = 0
    print(selector)
    while cnt < 280:
        cnt += 1
        for cmd in motor_commands[selector]:
            outputCommand(cmd)


def readButtons():
    time.sleep(0.2)
    btns = [
        GPIO.input(buttons[0]),
        GPIO.input(buttons[1]),
        GPIO.input(buttons[2]),
        GPIO.input(buttons[3])
    ]
    return btns


def takePicture():
    camera.capture('/home/pi/Desktop/image.jpg')
#     time.sleep(1)
    print('picture_taken')


try:
    while True:
        btns = readButtons()
        if btns == [1,0,0,0]:
            rotate('forward1')
        elif btns == [0,1,0,0]:
            rotate('backward1')
        elif btns == [0,0,1,0]:
            rotate('forward2')
        elif btns == [0,0,0,1]:
            rotate('backward2')
        elif btns == [1,0,1,0]:
            rotate('forward')
        elif btns == [0,1,0,1]:
            rotate('backward')
        elif btns == [1, 1, 0, 0]:
            takePicture()
        else:
            outputCommand(idle)
except KeyboardInterrupt:
    print(exit)
    GPIO.cleanup()

