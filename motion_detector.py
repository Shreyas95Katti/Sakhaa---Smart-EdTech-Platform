
#importing necessary packages
import time
import argparse
import datetime
import imutils
import cv2
from imutils.video import VideoStream

#Construct the argument parser and parse the arguments
ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",help="Path to video file")
ap.add_argument("-a","--min-area",type=int,default=10000,help="Minimum area size")
args=vars(ap.parse_args())

#Read from webcam if video argument is none
if args.get("video",None) is None:
    vs=VideoStream(src=0).start()
    time.sleep(2.0)
#Otherwise read from the video file
else:
    vs=cv2.VideoCapture(args["video"])

#initialise first fram in the video to None
firstFrame=None

#loop over the frames of the video
while True:
    #take current frame and initialise to motion/stagnant
    frame=vs.read()
    frame=frame if args.get("video",None) is None else frame[1]
    text="stagnant"

    #To account for the possibility that we are playing a video,
    #we assume that if frame cannot be grabbed we have reached the end
    if frame is None:
        break

    #resize the frame, conver it to grayscale and blur it
    frame=imutils.resize(frame,width=500)
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    #if the first frame is None, initialise it
    if firstFrame is None:
        firstFrame=gray
        continue
    
    #compute absolute difference between first and current frame
    frameDelta=cv2.absdiff(firstFrame, gray)
    thresh=cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    #dilate threshold image to fill in the holes, then find contours
    thresh=cv2.dilate(thresh,None,iterations=2)
    cnts=cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)

    #loop over the contours
    for c in cnts:
        #if the contour is too small ignore it
        if cv2.contourArea(c)<args["min_area"]:
            continue

        #compute the bounding box for the contour, draw it on the frame,
        #and update the text
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        text="Motion Detected"

    #draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1) 

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    #if 'q' is pressed,break the loop
    if key==ord("q"):
        break

#cleanup the cmaera and close all windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()  
