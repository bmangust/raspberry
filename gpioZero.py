from gpiozero import Button, LED
from signal import pause

led = LED(6)
button = Button(21)

button.when_pressed = led.on
button.when_released = led.off

pause()