import RPi.GPIO as G

buttons = [2, 3, 4, 8]
leds = [13, 19, 16, 14, 15, 17, 18, 10, 24, 12, 21, 26]

G.setmode(G.BCM)
for i in leds:
    G.setup(i, G.OUT)
for b in buttons:
    G.setup(b, G.IN)

#pwm = G.PWM(13, 1000)
#dutyCycle = 50
#pwm.start(dutyCycle)

def isPressed (btn, led):
    if (G.input(btn) == False):
	G.output(led, G.HIGH)
    else:
	G.output(led, G.LOW)


while (True):
    if (not G.input(buttons[0])):
        break
    for i in range(1, 4):
        isPressed(buttons[i], leds[i-1])
    #time.sleep(delay)
    #dutyCycle = dutyCycle + 1
    #if (dutyCycle > 100):
    #    dutyCycle = 0
    #pwm.ChangeDutyCycle(dutyCycle)

G.cleanup()
