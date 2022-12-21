import cv2

# set up camera object
cap = cv2.VideoCapture(0)

# QR code detection object
detector = cv2.QRCodeDetector()
data = None
bbox = None
while True:
    # get the image
    _, img = cap.read()
    # get bounding box coords and data
    if(cv2.waitKey(1) & 0xFF == ord("r")):
        data, bbox, _ = detector.detectAndDecode(img)
        if(bbox is not None):
            bbox = bbox[0]
    else:
        print("Press r to read")

    # if there is a bounding box, draw one, along with the data
    if(bbox is not None):
        for i in range(len(bbox)):
            print(bbox)
            cord_p1 = tuple(bbox[i])
            cord_p2 = tuple(bbox[(i+1) % len(bbox)])
            print((int(cord_p1[0]),int(cord_p1[1])))
            print((int(cord_p2[0]),int(cord_p2[1])))
            cv2.line(img, (int(cord_p1[0]),int(cord_p1[1])), (int(cord_p2[0]),int(cord_p2[1])), color=(255, 0, 255), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0]), int(bbox[0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
        if data:
            print("data found: ", data)
    # display the image preview
    cv2.imshow("code detector", img)
    if(cv2.waitKey(1) == ord("q")):
        break
# free camera object and exit
cap.release()
cv2.destroyAllWindows()