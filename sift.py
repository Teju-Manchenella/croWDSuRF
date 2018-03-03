import numpy as np
import cv2 as cv


gray = cv.imread('a.jpg',0)

# gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)

sift = cv.xfeatures2d.SIFT_create()

kp = sift.detect(gray,None)

img=cv.drawKeypoints(gray,kp,img)
cv.imwrite('sift_keypoints.jpg',img)
