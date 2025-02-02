import cv2


def motion():
    cap = cv2.VideoCapture(0)
    ret, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    thresh = 65

    while True:
        ret, frame2 = cap.read()
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        
        _, thresh_frame = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        
        
        cv2.imshow('Motion Detection', frame2)
        
        gray1 = gray2
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
