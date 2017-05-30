import cv2
import numpy as np
import argparse

refPt = []
cropping = False


cap = cv2.VideoCapture(2)
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
        print  refPt
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        print refPt
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)



while True:
    # display the image and wait for a keypress
    _, image = cap.read()
    clone = image.copy()
    cv2.imshow("image", image)

    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        target = image
        hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

        # calculating object histogram
        roihist = cv2.calcHist([hsv], [0,1], None, [180, 256], [0, 180, 0, 256])

        # normalize histogram and apply backprojection
        cv2.normalize(roihist, roihist, 0, 255, cv2.NORM_MINMAX)
        dst = cv2.calcBackProject([hsvt], [0, 1], roihist, [0, 180, 0, 256], 1)

        # Now convolute with circular disc
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cv2.filter2D(dst, -1, disc, dst)

        # threshold and binary AND
        ret, thresh = cv2.threshold(dst, 50, 255, 0)
        thresh = cv2.merge((thresh, thresh, thresh))
        res = cv2.bitwise_and(target, thresh)
        res = np.vstack((target, thresh, res))
        cv2.imshow("final",res)
    # if the 'c' key is pressed, break from the loop
    elif cv2.waitKey(1) & 0xFF == ord("c"):
        break



# close all open windows
cv2.destroyAllWindows()