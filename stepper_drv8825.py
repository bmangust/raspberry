import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
buttons = [6, 13]
# mstep = [7,8,25]
STEP = 21
DIR  = 20
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

for button in buttons:
    GPIO.setup(button, GPIO.IN)
# for pin in mstep:
#     GPIO.setup(pin, GPIO.OUT)
    
# MODE = (25, 8, 7)   # Microstep Resolution GPIO Pins
# GPIO.setup(MODE, GPIO.OUT)
# RESOLUTION = {'Full': (0, 0, 0),
#               'Half': (1, 0, 0),
#               '1/4': (0, 1, 0),
#               '1/8': (1, 1, 0),
#               '1/16': (0, 0, 1),
#               '1/32': (1, 0, 1)}
# GPIO.output(MODE, RESOLUTION['1/32'])


CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

step_count = SPR
delay = 0.01


try:
    GPIO.output(DIR, GPIO.HIGH)
    while (True):
        btn = GPIO.input(buttons[0])
        if (btn):
            GPIO.output(STEP, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            time.sleep(delay)


    '''
    while True:
        forward = GPIO.input(buttons[0])
        back = GPIO.input(buttons[1])
        if forward:
            GPIO.output(mdir, GPIO.HIGH)
        else:
            GPIO.output(mdir, GPIO.LOW)
        while back:
    
    

    GPIO.output(DIR, CW)
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)

    time.sleep(.5)
    GPIO.output(DIR, CCW)

    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)
    '''
except KeyboardInterrupt:
    print(exit)
finally:
    GPIO.cleanup()
