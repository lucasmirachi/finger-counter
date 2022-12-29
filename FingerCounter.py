import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import os

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)

#to store the finger images
folderPath = "images"
imgList = sorted(os.listdir(folderPath))
print(imgList)
overlayList = []
for imgPath in imgList:
    img = cv2.imread(f'{folderPath}/{imgPath}')
    print(f'{folderPath}/{imgPath}')
    overlayList.append(img)
    #print(len(overlayList))

detector = htm.handDetector()

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarksList, bbox = detector.findPositions(img,draw=False)

    if len(landmarksList) != 0:
        fingers = []
        #because it is physically very hard to put the thumb down, we're gonna treat it separately fom the other fingers
        #THUMB
        if landmarksList[tipIds[0]][1] > landmarksList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #4 FINGERS
        for id in range(1,5):
            if landmarksList[tipIds[id]][2] < landmarksList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)

        totalFingers = fingers.count(1)
        print(totalFingers)

        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

        cv2.rectangle(img, (0,265), (130,425), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (15, 400), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}' , (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3) 
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break