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
    UnauthorizedError
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

def grantOperatorAccess():
    print("Access: Operator Level granted")
    messageBody = {
        "lockerState": "open"
    }
    ipcClient.publishMessage(json.dumps(messageBody),"cmd/locker/operator")

def lockerControl(acess_level):
        if(acess_level == 1):
            grantOperatorAccess()
        elif(access_level == 2):
            grantMaintenaceAccess()
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
    lockerControl(authObj["acess_level"])

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
    bodyStr, bodyJsonObject = decodeJsonMessage(eventJsonObj["body"]) 
    qrPayloadStr, qrJsonObj = decodeJsonMessage(bodyJsonObject["message"])
    #print("Final qr Data:")
    #print(qrJsonObj)
    return qrJsonObj

def handleQrCode(event):
    eventPayload = ipcClient.returnEventMessage(event)    
    
    qrCodeData = getQrDataFromPayload(eventPayload)  
    
    if newUserEvent(qrCodeData):
        qrCodeAuth(qrCodeData)
    else:
        print("User Already Authenticated")

#ipcClient.subscribeCallbackMethod(handleBlinkyStatus)

ipcClient.subscribeToTopic("status/blinky",handleBlinkyStatus)

ipcClient.subscribeToTopic("data/QrCode/Cam1",handleQrCode) 

try:
    while True:
        sleep(1)
        print("Listening to topics.")
except InterruptedError:
    print('Subscribe interrupted.')