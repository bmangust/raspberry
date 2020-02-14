import RPi.GPIO as GPIO
import time
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
halfstep_bk_1 = [
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
halfstep_bk_2 = [
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
fullstep_bk_1 = [
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
fullstep_bk_2 = [
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
fullstep_bk = [
  [0,0,0,1,0,0,0,1],
  [0,0,1,0,0,0,1,0],
  [0,1,0,0,0,1,0,0],
  [1,0,0,0,1,0,0,0]
]

idle = [0,0,0,0,0,0,0,0]

"""
forward = [
    [1,0,0,0,0,1,1,1],
    [1,1,0,0,0,0,1,1],
    [1,1,1,0,0,0,0,1],
    [1,1,1,1,0,0,0,0],
    [0,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,0],
    [0,0,0,0,1,1,1,1],
]
"""

def pulsePin(pin):
    GPIO.output(pin, 1)
    time.sleep(0.001)
    GPIO.output(pin, 0)
    

def outputCommand(cmd):
    for bit in cmd:
        GPIO.output(dataPin, bit)
        pulsePin(clockPin)
        time.sleep(0.00001)
    pulsePin(latchPin)



try:
    while True:
        btns = [
            GPIO.input(buttons[0]),
            GPIO.input(buttons[1]),
            GPIO.input(buttons[2]),
            GPIO.input(buttons[3])
        ]
        if btns == [1,0,0,0]:
            for cmd in fullstep_fw_1:
                #print(cmd)
                outputCommand(cmd)
                #time.sleep(0.01)
        elif btns == [0,1,0,0]:
            for cmd in fullstep_bk_1:
                #print(cmd)
                outputCommand(cmd)
                #time.sleep(0.1)
        elif btns == [0,0,1,0]:
            for cmd in fullstep_fw_2:
                #print(cmd)
                outputCommand(cmd)
                #time.sleep(0.01)
        elif btns == [0,0,0,1]:
            for cmd in fullstep_bk_2:
                #print(cmd)
                outputCommand(cmd)
                #time.sleep(0.1)
        elif btns == [1,0,1,0]:
            for cmd in fullstep_fw:
                #print(cmd)
                outputCommand(cmd)
                #time.sleep(0.01)
        elif btns == [0,1,0,1]:
            for cmd in fullstep_bk:
                #print(cmd)
                outputCommand(cmd)
                #time.sleep(0.01)
        else:
            #print(idle)
            outputCommand(idle)
        time.sleep(0.0001)            
except KeyboardInterrupt:
    print(exit)
    GPIO.cleanup()

