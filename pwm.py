import RPi.GPIO as G
import time

G.setmode(G.BCM)
G.setup(13, G.OUT)
G.setup(2, G.IN)
pwm = G.PWM(13, 1000)
dutyCycle = 50
pwm.start(dutyCycle)

delay = 0.01
while (True):
    button = G.input(2)
    if (not button):
        break
    time.sleep(delay)
    dutyCycle = dutyCycle + 1
    if (dutyCycle > 100):
        dutyCycle = 0
    pwm.ChangeDutyCycle(dutyCycle)

G.cleanup()
