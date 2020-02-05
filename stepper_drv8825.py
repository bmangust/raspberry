import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
buttons = [14, 15]
reset = 6
slp = 13
step = 19
mdir  = 26
fault = 18
GPIO.setup(step, GPIO.OUT)
GPIO.setup(mdir, GPIO.OUT)

for button in buttons:
    GPIO.setup(button, GPIO.IN)

try:
    while True:
        """
        forward = GPIO.input(buttons[0])
        back = GPIO.input(buttons[1])
        if forward:
            GPIO.output(mdir, GPIO.HIGH)
        else:
            GPIO.output(mdir, GPIO.LOW)
        while back:
            """
        GPIO.output(step, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(step, GPIO.LOW)
        time.sleep(0.001)
except KeyboardInterrupt:
    print(exit)
    GPIO.cleanup()
