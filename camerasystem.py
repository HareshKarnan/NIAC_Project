import numpy as np
mtx = np.matrix([[ 417.70843832,0,316.58646489],[0,417.85377461,248.56902084],[0,0,1]])
dist = np.matrix([[-0.38762883, 0.10970692, -0.00165442, -0.0013712,  -0.0070191 ]])
import nodesorter as node
import cv2
nodept=[]
def getnodes(img,pts1,pts2):
    # camera calibration
    nodept = []
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    img = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    img = img[y:y + h, x:x + w]

    # image warp
    M = cv2.getPerspectiveTransform(pts1, pts2)
    imgc = cv2.warpPerspective(img, M, (800, 600))

    # rotate image
    # (h, w) = imgc.shape[:2]
    # center = (w / 2, h / 2)
    # obj = cv2.getRotationMatrix2D(center, 180, 1.0)
    # imgc = cv2.warpAffine(imgc, obj, (w, h))

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
    # tval = cv2.getTrackbarPos('Threshold', 'mask')
    ret, thresh = cv2.threshold(result_image, 20, 255, 0)

    # find contours
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    temp = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            count = count + 1
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            nodept.append((cX, cY))

    # adding 3 extra nodes
    x1 = int((nodept[0][0] + nodept[1][0]) / 2);
    y1 = nodept[0][1] + 5;
    nodept.append((x1, y1))

    x2 = int((nodept[4][0] + nodept[5][0]) / 2);

    return nodept,imgc