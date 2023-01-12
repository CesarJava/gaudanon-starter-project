from time import sleep
import datetime
import json
import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import (
    BinaryMessage,
    PublishMessage,
    JsonMessage,
    SubscriptionResponseMessage,
    UnauthorizedError,
    PublishToIoTCoreRequest,
    QOS
    
)
import sys
import traceback
from IPCComm import IPCComm

ipcClient = IPCComm("GaudanonMachine","*")

lastUserId = None

def decodeJsonMessage(message):
    strMessage = "None"
    jsonObj = None    
    try:
        jsonObj = json.loads(message)
        strMessage = json.dumps(jsonObj)
    except Exception:
        strMessage = message
    
    return strMessage, jsonObj

def ipcMessageBody(message):
    strMessage, jsonObj = decodeJsonMessage(message["body"])
    return strMessage, jsonObj

def printQrCodeInfo(qrCodeObj):
    #print("Printing:\n")
    #print(qrCodeObj)
    print("User Requesting access: \n",
          "\tUser Name: ", qrCodeObj["name"],
          "\tUser Id: ", qrCodeObj["id"])
    

def grantOperatorAccess(userName=None,userRole=None):
    print("Access: Operator Level granted")
    messageBody = {
        "lockerAction": "open",
        "currentUserName": userName,
        "currentUserRole": userRole
    }
    ipcClient.publishMessage(json.dumps(messageBody),"cmd/locker1")
    
    messageBody["lockerAction"] = "close"
    
    ipcClient.publishMessage(json.dumps(messageBody),"cmd/locker2")

def grantMaintenaceAccess(userName=None,userRole=None):
    print("Access: Maintenace Level granted")
    messageBody = {
        "lockerAction": "open",
        "currentUserName": userName,
        "currentUserRole": userRole
    }
    ipcClient.publishMessage(json.dumps(messageBody),"cmd/locker1")
    
    ipcClient.publishMessage(json.dumps(messageBody),"cmd/locker2")

def lockerControl(authObj=None):
        access_level = authObj["acess_level"]
        currentUsername = authObj["name"]
        currentUserRole = authObj["role"]
        if(access_level == 1):
            grantOperatorAccess(currentUsername, currentUserRole)
        elif(access_level == 2):
            grantMaintenaceAccess(currentUsername, currentUserRole)
        else:
            lockEverything()
            
def newUserEvent(qrCodeData):
    global lastUserId
    if lastUserId != qrCodeData["id"]:
        lastUserId = qrCodeData["id"]
        return True
    else:
        return False

def qrCodeAuth(authObj):      
    printQrCodeInfo(authObj)
    lockerControl(authObj)

def handleBlinkyStatus(event):
    message = ipcClient.returnEventMessage(event)
    
    statusMessage, jsonObj = decodeJsonMessage(message)
        
    print("Status: ", statusMessage)

#"{
#    "timestamp": str(datetime.datetime.now()),
#    "clientId": str(self.clientId),
#    "body": "{
    #   'message': '{
        #   "id": "1504bb2461df4a478f25b9367880dff7",
        # "role": "Operator",
        # "name": "John Doing Doe",
        # "acess_level": 1
        # }'
    # }" 
#}""

def getQrDataFromPayload(eventPayload):
    eventPayloadStr , eventJsonObj = decodeJsonMessage(eventPayload)
   
    qrPayloadStr, qrJsonObj = decodeJsonMessage(eventJsonObj["body"])
    #print("Final qr Data:")
    #print(qrJsonObj)
    return qrJsonObj

def publishQrCodeToCloud(eventPayload):
    topic = "data/gaudanon/status/machine/qrcode"
    ipcClient.publishToIoTCore(topic, '1', eventPayload)


def handleQrCode(event):
    eventPayload = ipcClient.returnEventMessage(event)    
    
    qrCodeData = getQrDataFromPayload(eventPayload)  
    
    if newUserEvent(qrCodeData):
        qrCodeAuth(qrCodeData)
    else:
        print("User Already Authenticated")
        
    publishQrCodeToCloud(eventPayload)

def handleLockerStatus(event):
    eventPayload = ipcClient.returnEventMessage(event) 
    print("Locker Status: ", eventPayload)
    if (json.loads(eventPayload)["clientId"] == "Locker1"):
        topic = "data/gaudanon/status/machine/locker1"
    elif (json.loads(eventPayload)["clientId"] == "Locker2"):
        topic = "data/gaudanon/status/machine/locker2"
    ipcClient.publishToIoTCore(topic, '1', eventPayload)

#ipcClient.subscribeCallbackMethod(handleBlinkyStatus)

ipcClient.subscribeToTopic("status/blinky",handleBlinkyStatus)

ipcClient.subscribeToTopic("data/QrCode/Cam1",handleQrCode) 

ipcClient.subscribeToTopic("status/locker1",handleLockerStatus)

ipcClient.subscribeToTopic("status/locker2",handleLockerStatus) 


try:
    while True:
        sleep(1)
        print("Listening...")
except InterruptedError:
    print('Subscribe interrupted.')