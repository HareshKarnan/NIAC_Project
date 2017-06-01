import cv2
import numpy as np
import time
import nodesorter as node
import math
from operator import itemgetter
import camerasystem
import control
import threading

x_point = []
y_point = []
cap = cv2.VideoCapture(1)
mtx = np.matrix([[ 417.70843832,0,316.58646489],[0,417.85377461,248.56902084],[0,0,1]])
dist = np.matrix([[-0.38762883, 0.10970692, -0.00165442, -0.0013712,  -0.0070191 ]])
def nothing(x):
    pass


def get_pixel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print x, y
        x_point.append(x)
        y_point.append(y)

        # create calibration window


cv2.namedWindow('Calibration', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Calibration', get_pixel)
cv2.resizeWindow('Calibration', 800, 600)

while (len(x_point) <= 3):
    # get first frame
    ret, img = cap.read()

    #camera calibration
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    img = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    img = img[y:y + h, x:x + w]

    #define corners
    cv2.putText(img, "Select points to define corners", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))
    cv2.imshow('Calibration', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if len(x_point) > 3:
        cv2.destroyAllWindows()
        print "black", x_point[0], y_point[0]
        pts1 = np.float32(
            [[x_point[0], y_point[0]], [x_point[1], y_point[1]], [x_point[2], y_point[2]], [x_point[3], y_point[3]]])
        pts2 = np.float32([[0, 0], [800, 0], [0, 600], [800, 600]])
        break


def nothing(x):
    pass
# create other windows for image and mask
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 800, 600)

cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.resizeWindow('mask', 800, 600)
#cv2.createTrackbar('Threshold', 'mask',0,255,nothing)

def getkey(item):
    return item[0]+item[1]
while (len(x_point) > 3):
    start_time = time.time()
    # Capture frame-by-frame
    ret, img = cap.read()
    nodept,imgc = camerasystem.getnodes(img,pts1,pts2)

    #sorting done here
    nodept.sort(key=itemgetter(1),reverse=True)

    try :
            print nodept
            nodept = node.dist_scan(nodept,nodept_old)

    except (RuntimeError, TypeError, NameError):
        print "first time skip"
        pass
    # write node numbers and draw circles
    temp = 0
    for pt in nodept:
            temp = temp+1
            cv2.putText(imgc, str(temp), pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))
            cv2.circle(imgc, pt, 4, (100, 100, 10), thickness=5)

    nodept_old = nodept
    #print "stored"
    nodept=[]


    #display image in window
    cv2.imshow('image', imgc)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #print("--- %s Hertz ---" % pow((time.time() - start_time),-1) )
