import RPi.GPIO as G
import time

G.setmode(G.BCM)
G.setup(13, G.OUT)
G.setup(19, G.OUT)
G.setup(16, G.OUT)

delay = 0.1
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

G.cleanup()
