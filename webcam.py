import numpy as np
import cv2
import time


cap = cv2.VideoCapture(1)
start_time = time.time()
skip = 60


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    if time.time() - start_time > skip:
        name= "pics/dat_%s.jpeg" % time.strftime("%Y%m%d_%H_%M_%S")
        #print "printing"
        start_time = time.time()
        cv2.imwrite(name, frame)


cap.release()
cv2.destroyAllWindows()


