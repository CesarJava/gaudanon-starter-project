from gpiozero import LED
from time import sleep

white = LED(17)

while True:
    white.on()
    sleep(1)
    white.off()
    sleep(1)