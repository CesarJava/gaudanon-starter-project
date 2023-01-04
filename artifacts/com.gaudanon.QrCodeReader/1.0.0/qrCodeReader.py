import cv2
from pyzbar.pyzbar import decode
import numpy as np
import awsiot.greengrasscoreipc
from time import sleep
from IPCComm import IPCComm
import json

camera_id = 0
delay = 0.2
window_name = "Detecting with Open CV"

ipcClient = IPCComm("QrCodeCamera","data/QrCode/Cam1")

# set up camera object
cap = cv2.VideoCapture(camera_id)

# QR code detection object
qcd = cv2.QRCodeDetector()

def decodeImages(rawImage):
    codesRead = []
    for decodedImage in decode(image):
        codesRead.append(decodedImage)
    return codesRead

def pointsTo32bitArray(pointsArray):
    points = [[point.x, point.y] for point in pointsArray]
    points = np.array(points, np.int32)
    return points

def getPointsArray(decodedImage):
    pointsArray = decodedImage.polygon
    points = pointsTo32bitArray(pointsArray)
    return points

def drawInWindow(image, codesRead):
    for code in codesRead:
        points = getPointsArray(code)
        image = cv2.polylines(image,[points], True, (0,255,0), 3)

def getDataFromImage(image):
    qrCodeData = image.data.decode()
    print("Data Read: \n", qrCodeData)
    return qrCodeData

def processQrCodes(codes):
    if (len(codes) > 1):
        print("Won't process more than 1 code at a time.")
    elif (len(codes) == 1):
        firstCodeImage = codes[0]
        codeData = getDataFromImage(firstCodeImage)
        reportCodeRead(codeData)
    else:
        print("waiting for code")

def reportCodeRead(codeData):
    messageBody = {
        "message": codeData
    }
    publishMessageIpc(messageBody)

def publishMessageIpc(message):
    ipcClient.setMessage(json.dumps(message))
    ipcClient.publishMessage()

while True:
    # get the image
    isImageCaptured, image = cap.read()


    if isImageCaptured:
        codesRead = decodeImages(image)
        processQrCodes(codesRead)
        sleep(1)
    #    drawInWindow(image, codesRead)
        
    #    cv2.imshow(window_name, image)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

cap.release()
#cv2.destroyWindow(window_name)


