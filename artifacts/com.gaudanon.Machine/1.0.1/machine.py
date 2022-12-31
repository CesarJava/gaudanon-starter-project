import time
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

def reportStatus(message):
    statusMessage = "None"
    try:
        jsonObj = json.loads(message)
        statusMessage = json.dumps(jsonObj)
    except Exception:
        statusMessage = message
        
    print("Status: ", statusMessage)

ipcClient.subscribeCallbackMethod(reportStatus)

ipcClient.subscribeToTopic("status/blinky")