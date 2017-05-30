import cv2
import numpy as np
import time
import math
from operator import itemgetter
import control
import threading

x_point = []
y_point = []
cap = cv2.VideoCapture(0)
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
nodept=[]
def getkey(item):
    return item[0]+item[1]
while (len(x_point) > 3):
    start_time = time.time()
    # Capture frame-by-frame
    ret, img = cap.read()

    # camera calibration
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    img = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    img = img[y:y + h, x:x + w]

    # image warp
    M = cv2.getPerspectiveTransform(pts1, pts2)
    imgc = cv2.warpPerspective(img, M, (800, 600))

    # rotate image
    #(h, w) = imgc.shape[:2]
    #center = (w / 2, h / 2)
    #obj = cv2.getRotationMatrix2D(center, 180, 1.0)
    #imgc = cv2.warpAffine(imgc, obj, (w, h))

    # convert to hsv format
    hsv = cv2.cvtColor(imgc, cv2.COLOR_BGR2HSV)

    # set the values for red
    lower_green = np.array([1, 80, 80], dtype=np.uint8)
    upper_green = np.array([10, 255, 255], dtype=np.uint8)

    # create a mask image
    mask_img = cv2.inRange(hsv, lower_green, upper_green)

    resu = cv2.bitwise_and(imgc, imgc, mask=mask_img)
    result_image = cv2.cvtColor(resu, cv2.COLOR_BGR2GRAY)

    # image thresholding
    #tval = cv2.getTrackbarPos('Threshold', 'mask')
    ret, thresh = cv2.threshold(result_image, 20, 255, 0)

    # find contours
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    count =0
    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            count=count+1
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            nodept.append((cX,cY))
            cv2.circle(imgc,(cX,cY),4,(100,100,10),thickness=5)
    temp=0
    nodept.sort(key=itemgetter(1))
    for pt in nodept:
        temp=temp+1
        cv2.putText(imgc,str(temp) , pt, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))

    #number the nodes

    cv2.imshow('image', imgc)
    cv2.imshow('mask', thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print nodept
        break
    nodept=[]
    print("--- %s seconds ---" % pow((time.time() - start_time),-1) )
