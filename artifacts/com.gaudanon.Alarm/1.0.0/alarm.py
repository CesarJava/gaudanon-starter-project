from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
from IPCComm import IPCComm
import json


factory = PiGPIOFactory()
buzzer = TonalBuzzer(16, pin_factory=factory)

ipcClient = IPCComm("Alarm","cmd/gaudanon/machine/alarm")

def playAlarmSound():
    buzzer.play("G5")
    sleep(0.5)
    buzzer.play("E5")
    sleep(0.25)
    buzzer.play("C5")
    sleep(0.5)
    buzzer.play("A5")
    sleep(0.5)
    buzzer.play("G5")
    sleep(0.8)
    buzzer.play("E5")
    sleep(0.25)
    buzzer.play("G5")
    sleep(0.125)
    buzzer.play("F5")
    sleep(0.25)
    buzzer.play("G5")
    sleep(0.125)
    buzzer.play("F5")
    sleep(0.25)
    buzzer.play("D5")
    sleep(0.25)
    buzzer.play("E5")
    sleep(0.125)
    buzzer.stop()
    sleep(0.2)

def handlerAlarmComand(event):
    if (event):
        playAlarmSound()

ipcClient.subscribeToIotTopic("cmd/gaudanon/machine/alarm", handlerAlarmComand)

while True:
    print("Waiting Alarms")
    sleep(1)