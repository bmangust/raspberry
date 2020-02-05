import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
buttons = [14, 15]
control_pins = [6,13,19,26]
for button in buttons:
    GPIO.setup(button, GPIO.IN)
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
halfstep_fw = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]
halfstep_bk = [
  [0,0,0,1],
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0],
  [1,0,0,1]
]


try:
    while True:
        forward = GPIO.input(buttons[0])
        back = GPIO.input(buttons[1])
        if forward:
          for halfstep in range(8):
            for pin in range(4):
              GPIO.output(control_pins[pin], halfstep_fw[halfstep][pin])
            time.sleep(0.0005)
        elif back:
          for halfstep in range(8):
            for pin in range(4):
              GPIO.output(control_pins[pin], halfstep_bk[halfstep][pin])
            time.sleep(0.0005)
except KeyboardInterrupt:
    print(exit)
    GPIO.cleanup()
