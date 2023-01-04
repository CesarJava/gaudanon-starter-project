from gpiozero import Button, AngularServo
from time import sleep
from signal import pause
import sys
from IPCComm import IPCComm
import json

ipcClient = IPCComm("Locker1","cmd/locker1")

#
# Arg Settings
#

#servoPort = (21, sys.argv[1])[len(sys.argv)>=2]

servoPort = sys.argv[1] if len(sys.argv) >= 2 else 21

unlockedPort = sys.argv[3] if len(sys.argv) >= 4 else 19

lockedPort = sys.argv[2] if len(sys.argv) >= 3 else 26

activatePort = sys.argv[4] if len(sys.argv) >= 5 else 20


#
# GPIO Vars
#
servo = AngularServo(servoPort, min_angle =-90, max_angle=90)

locked = Button(lockedPort)
unlocked = Button(unlockedPort)

activate = Button(activatePort)

lockingState = "DOOR LOCKED" if locked.is_pressed else "DOOR UNLOCKED"

currentUser = "NoUser"
previousUser = "NoUser"
#
#
#

def setLockingState(state):
    global lockingState
    validStates = ["LOCKED","UNLOCKED","LOCKING", "UNLOCKING"]
    if(state in validStates):
        lockingState = state
    
    reportLockState()

def itShouldBeLocking():
    return lockingState == "LOCKING"

def itShouldBeUnlocking():
    return lockingState == "UNLOCKING"     

def stopLockingWhenPressed():
    global servo, lockingState
    if(itShouldBeLocking()):
        setLockingState("LOCKED")
        servo.angle = 0

def stopUnlockingWhenPressed():
    global servo, lockingState
    if(itShouldBeUnlocking()):
        setLockingState("UNLOCKED")
        servo.angle = 0
    
def unlock():
    setLockingState("UNLOCKING")
    servo.angle = 45

def lock():
    setLockingState("LOCKING")
    servo.angle = -45    

def changeLockState():
    global servo, lockingState
    if (locked.is_pressed):
        unlock()
    elif(unlocked.is_pressed):
        lock()
    
def setup():
    global locked, unlocked, activate
    locked.when_pressed = stopLockingWhenPressed
    unlocked.when_pressed = stopUnlockingWhenPressed
    activate.when_pressed = changeLockState

setup()

def decodeJsonMessage(message):
    strMessage = "None"
    jsonObj = None    
    try:
        jsonObj = json.loads(message)
        strMessage = json.dumps(jsonObj)
    except Exception:
        strMessage = message
    
    return strMessage, jsonObj

def handleLockerAction(eventPayload):
    print("New Action Received")
    action = eventPayload["lockerAction"]
        
    if(action == "open"):
        unlock()
    elif(action ==  "close"):
        lock()
    else:
        lock()
    
def handleUserExchange(eventPayload):
    global currentUser, previousUser
    currentUserReceived = None
    try:
        currentUserReceived= str(eventPayload["currentUserName"])
        print("Handling user exchange for: "+currentUserReceived)
    except Exception:
        print("Invalid user name. Must be String.")
        return
    
    previousUser = currentUser
    currentUser  = currentUserReceived   
        
def handlerLockCommand(event):
    print("Event:")
    print(event)
    eventPayload = json.loads(ipcClient.returnEventMessage(event))
    
    #eventMessageStr , eventJsonObj = decodeJsonMessage(eventPayload)
    print("Event Payload:")
    print(eventPayload)
    
    handleLockerAction(eventPayload)
    handleUserExchange(eventPayload)

ipcClient.subscribeToTopic("cmd/locker1", handlerLockCommand)

def publishMessageIpc(message):
    ipcClient.setMessage(message)
    ipcClient.publishMessage(topicToPublish="status/locker1")

def reportLockState():
    global lockingState, currentUser, previousUser
    lockStateBody = {
        "id": 1,
        "name": "OperatorLocker",
        "currentState": lockingState,
        "operatorName": currentUser,
        "previousUserName": previousUser
    }
    publishMessageIpc(lockStateBody)
       
while True:
    print("Servo: %s Door State: %s Locked: %s Unlocked: %s Activate: %s"%(servo.angle,lockingState,locked.is_pressed, unlocked.is_pressed, activate.is_pressed))
    reportLockState()
    sleep(10)
    
    
    
    
    
    
    
    #servo.angle = turn
    #if(not locked and lock_state.is_pressed):
    #    turn = 0
    #    print("Locked")
    #    print("Running Locked:"+str(locked)+" Open:"+str(open)+" Activated:"+str(activated)+" Angle:"+str(servo.angle))       
    #if(not open and open_state.is_pressed):
    #    turn = 0
    #    print("Opened")        
    #    print("Running Locked:"+str(locked)+" Open:"+str(open)+" Activated:"+str(activated)+" Angle:"+str(servo.angle))
    #if(not activated and activate_state.is_pressed):
    #    print("Activated")
    #    print("Running Locked:"+str(locked)+" Open:"+str(open)+" Activated:"+str(activated)+" Angle:"+str(servo.angle))
    #    if(lock_state.is_pressed):
    #        print("Opening")
    #        turn = 45
    #    elif(open_state.is_pressed):
    #        print("Locking")
    #        turn = -45
    #    else:
    #        turn = 0
    #activated = activate_state.is_pressed
    #locked = lock_state.is_pressed
    #open = open_state.is_pressed
    