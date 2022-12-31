from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import LED
from time import sleep
from IPCComm import IPCComm
import json


factory = PiGPIOFactory()
white = LED(17, pin_factory=factory)

ipcClient = IPCComm("Blinky","status/blinky")

messageBody = {
    "message": "beat"
}

ipcClient.setMessage(json.dumps(messageBody))

def publishBeatMessage():
    ipcClient.publishMessage()

def blinkLED():
    white.on()
    sleep(1)
    white.off()
    sleep(1)
    
while True:
    publishBeatMessage()
    blinkLED()
    