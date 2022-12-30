from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED
from time import sleep
from IPCComm import IPCComm


factory = PiGPIOFactory()
white = LED(17, pin_factory=factory)

ipcClient = IPCComm("Blinky","status/blinky")


while True:
    ipcClient.publishMessage("beat")
    white.on()
    sleep(1)
    white.off()
    sleep(1)