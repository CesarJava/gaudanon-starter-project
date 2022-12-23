from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED
from time import sleep

factory = PiGPIOFactory()
white = LED(17, pin_factory=factory)

while True:
    white.on()
    sleep(1)
    white.off()
    sleep(1)