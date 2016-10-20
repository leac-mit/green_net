import numpy as np
import pdb
import cv2
import time

RECORD = True
LIVE = True
if LIVE:
    cap = cv2.VideoCapture(1)
else:
    cap = cv2.VideoCapture("output.avi")
start_time = time.time()
skip = 60

if RECORD:
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out1 = cv2.VideoWriter('output1.avi',fourcc, 20.0, (640,480))
    out2= cv2.VideoWriter('output2.avi',fourcc, 20.0, (640,480))


def get_vals( img, (x,y,w,h)):
    mask = np.zeros(img.shape, np.uint8)
    mask[y:y+h, x:x+w] =  img[y:y+h, x:x+w]

    vals = mask[y:y+h, x:x+w]
    info = np.mean(vals)#, np.max(vals), np.min(vals)

    return mask, info

block1 = (100, 90, 300, 200)

b1 = (249, 174, 10,10)
b2 = (175, 183, 10,10)
b3 = (140,150, 10,10)

def clicked(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN :
        print "down:", x,y
    if event == cv2.EVENT_LBUTTONUP:
        print "up", x,y

cv2.namedWindow("image")
cv2.setMouseCallback("image", clicked)
i = 0
ret = False

RECORD = True
LIVE = True

while cap.isOpened():
    i += 1

    if not LIVE:
        if i %100 == 0:
            ret, frame = cap.read()
        else: 
            time.sleep(.001)
            continue
        if ret:
            frame = cv2.flip(frame, 0)
        else:
            cap = cv2.VideoCapture("output.avi")
            continue
    else:
            ret, frame = cap.read()

    kernel = np.ones((7,7),np.float32)/25
    frame = cv2.filter2D(frame,-1,kernel)
    frame = cv2.medianBlur(frame,5)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    maskb1,b1avg = get_vals(gray, b1)
    maskb2,b2avg = get_vals(gray, b2)
    maskb3,b3avg = get_vals(gray, b3)
    isUp =  abs(b1avg - b3avg) > abs(b2avg - b3avg)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(frame,(135, 80),(290, 250),(255,0,0),3)
    rows,cols = gray.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    frame = cv2.warpAffine(frame,M,(cols,rows))
    
    status = "Light switch 1 ON" if isUp else "Light switch 1 OFF"
    status2 = "%d Watts" % ( 112 if isUp else 0)
    cv2.putText(frame,status,(100,200), font, 1,(255,0,0),2)
    cv2.putText(frame,status2,(100,240), font, 1,(255,0,0),2)
    

    cv2.imshow('b1', maskb1)
    cv2.imshow('b2', maskb2)
    cv2.imshow('b3', maskb3)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask1, info = get_vals( gray, block1)
    
    
    gray = cv2.Canny(frame, 100, 200)

    cv2.imshow('image', frame)
    cv2.imshow('image2', gray)
    #cv2.imshow('image3', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if RECORD:
        out1.write(frame)
        out2.write(gray)
    """
    if time.time() - start_time > skip:
        name= "pics/dat_%s.jpeg" % time.strftime("%Y%m%d_%H_%M_%S")
        #print "printing"
        start_time = time.time()
        cv2.imwrite(name, frame)
    """

cap.release()
cv2.destroyAllWindows()


