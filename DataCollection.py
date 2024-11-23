import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 256
folder = "Data_256x256/A"
counter = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0] # hand[0] as only one hand is identified.
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize,3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset] # y = height , x = width , offset = extra  
        imgCropShape = imgCrop.shape
        aspectRatio = h / w

        if aspectRatio > 1: #height>width stretch the height to imgsize and set width accordingly and center the image crop onto imgwhite
            k = imgSize / h # k = constant
            wCal = math.ceil(k * w) #calculated width
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
        
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg',imgWhite)
        print(counter)