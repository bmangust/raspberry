import RPi.GPIO as G
import time

G.setmode(G.BCM)
G.setup(2, G.IN)
G.setup(13, G.OUT)
G.setup(19, G.OUT)
G.setup(16, G.OUT)

delay = 0.1
while (True):
    time.sleep(0.1)
    button = G.input(2)
    if not button:
        i = 0
        while(i < 10):
            i += 1;
            time.sleep(delay)
            G.output(13, G.HIGH)
            time.sleep(delay)
            G.output(19, G.HIGH)
            time.sleep(delay)
            G.output(16, G.HIGH)
            time.sleep(delay)
            G.output(13, G.LOW)
            time.sleep(delay)
            G.output(19, G.LOW)
            time.sleep(delay)
            G.output(16, G.LOW)
    else:
        G.output(13, G.LOW)
        G.output(19, G.LOW)
        G.output(16, G.LOW)

G.cleanup()
