import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

def board():
        
    folderPath = "Header"
    myList = os.listdir(folderPath)
    #print(myList)
    overlayList = []

    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)

    header = overlayList[0]
    drawColour = (255, 0, 255)
    brushThickness = 10
    eraserThickness = 100

    u_green = np.array([94, 80, 2])
    l_green = np.array([120, 255, 255])


    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = htm.handDetector(detectionCon = 0.85)
    xp, yp = 0, 0

    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    bg = cv2.imread("Lenna.png")
    bg = cv2.resize(bg, (1280, 720))

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        #GreenScreen
        mask = cv2.inRange(frame, l_green, u_green)
        res = cv2.bitwise_and(frame, frame, mask = mask)
        frame = frame - res
        frame = np.where(frame == 0, bg, frame)

        #Find HandLandmarks
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame, draw = False)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]         #Tip of index
            x2, y2 = lmList[12][1:]        #Tip of Middle

            
            #Check for Fingers
            fingers = detector.fingersUp()
            #print(fingers)

            #If select 2 finger
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                print("Selection Mode")
                
                #Check for click
                if y1 < 125:
                    if 250<x1<450:
                        header = overlayList[0]
                        drawColour = (0, 0, 255)
                    elif 550<x1<750:
                        header = overlayList[1]
                        drawColour = (0, 255, 0)
                    elif 880<x1<950:
                        header = overlayList[2]
                        drawColour = (255, 0, 0)
                    elif 1050<x1<1200:
                        header = overlayList[3]
                        drawColour = (0, 0, 0)

                cv2.rectangle(frame, (x1, y1-25), (x2, y2+25), drawColour, cv2.FILLED)

            #If draw 1 finger
            if fingers[1] and fingers[2] == False:
                cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColour == (0, 0, 0):
                    cv2.line(frame, (xp, yp), (x1, y1), drawColour, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColour, eraserThickness)
                    xp, yp = x1, y1
                else:
                    cv2.line(frame, (xp, yp), (x1, y1), drawColour, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColour, brushThickness)
                
                    xp, yp = x1, y1
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, imgInv)
        frame = cv2.bitwise_or(frame, imgCanvas)
        
        #Setting Header
        frame[0:125, 0:1280] = header
        #img = cv2.addWeighted(frame, 0.5, imgCanvas, 0.5, 0)
        cv2.imshow("Frame", frame)
        cv2.imshow("Writing", imgCanvas)
        if cv2.waitKey(1) == 27:
            break

def main():
    board()

if __name__=="__main__":
    main()
