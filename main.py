import cv2
import pickle
import cvzone
import numpy as np
import time

path = 'C:\\Users\\ThinkPad\\Desktop\\carPark.avi'
cap = cv2.VideoCapture(path)
width, height = 107, 48

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro):

    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count),
                           (x, y+height-3), scale=1.1, thickness=1, offset=0, colorR=(0, 0, 255))

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 3

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),
                      color, thickness)
    cvzone.putTextRect(img, f'Free: {spaceCounter} / {len(posList)}',
                       (100, 50), scale=3, thickness=2, offset=20, colorR=(0, 200, 0))

while True:
    pTime = 0
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpace(dilate)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

