import RPi.GPIO as GPIO
from time import sleep, time
from picamera import PiCamera
from PIL import Image, ImageStat
import imageio

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

current_position = 0
start_position = 0
end_position = 255

camera = PiCamera()
camera.resolution = (64, 64)

def pulsePin(pin):
    GPIO.output(pin, 1)
    sleep(0.0001)
    GPIO.output(pin, 0)
    

def outputCommand(cmd):
    for bit in cmd:
        GPIO.output(dataPin, bit)
        pulsePin(clockPin)
        sleep(0.00001)
    pulsePin(latchPin)


def rotateOneStep( direction ):
    global current_position
    current_position = 0
    if direction > 0:
        selector = 'forward1'
    else:
        selector = 'backward1'
    for i in range(5):
        for cmd in motor_commands[selector]:
            outputCommand(cmd)
        


def rotateToPosition( position ):
    global current_position
    cnt = 0
    steps = position - current_position
    if steps > -5 and steps < 5:
        return
    if steps <= -5:
        selector = 'forward1'
    elif steps >= 5:
        selector = 'backward1'
    steps = abs( steps )
#     print( selector )
    while cnt < steps:
        cnt += 1
        for cmd in motor_commands[selector]:
            outputCommand(cmd)
    current_position = position

# def rotate( selector ):
#     cnt = 0
#     print(selector)
#     while cnt < 280:
#         cnt += 1
#         for cmd in motor_commands[selector]:
#             outputCommand(cmd)


def readButtons():
    sleep(0.2)
    btns = [
        GPIO.input(buttons[0]),
        GPIO.input(buttons[1]),
        GPIO.input(buttons[2]),
        GPIO.input(buttons[3])
    ]
    return btns


def takePicture():
#     camera.image_effect = 'solarize'
    camera.capture('/home/pi/Desktop/image.jpg')
#     print('picture_taken')


def isDark(img):
    sum = 0
    for i in range(len(img)):
        row = []
        for j in range(len(img[i])):
            s = 0;
            for k in range(len(img[i][j])):
                s += img[i][j][k]
            s //= 3
            sum += s
    sum //= len(img) * len(img[0])
    print (sum)


def brightness( im_file ):
    im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def processImage():
    global current_position
    file = '/home/pi/Desktop/image.jpg'
    while ( True ):
        takePicture()
        br = brightness( file )
        print ( f'brigtnness: {br}, current: {current_position}' )
        rotateToPosition( br )
        if readButtons() == [0,1,0,0]:
            rotateToPosition(0)
            return

    

try:
    while True:
        btns = readButtons()
        if btns == [1,0,0,0]:
#             rotate('forward1')
            processImage()
        elif btns == [0,1,0,0]:
            break
#             rotate('backward1')
        elif btns == [0,0,1,0]:
            rotateOneStep( -1 )
        elif btns == [0,0,0,1]:
            rotateOneStep( 1 )
#             rotate('backward2')
#         elif btns == [1,0,1,0]:
#             rotate('forward')
#         elif btns == [0,1,0,1]:
#             rotate('backward')
#         elif btns == [1, 1, 0, 0]:
#             takePicture()
#             processImage()
        else:
            outputCommand(idle)
except KeyboardInterrupt:
    rotateToPosition( 0 )
    print(exit)
    GPIO.cleanup()

