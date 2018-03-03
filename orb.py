import cv2
import numpy as np
from matplotlib import pyplot as plt
import time


# start = time.clock()

img = cv2.imread('welch2.png')

# img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )


orb = cv2.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img,None)
# compute the descriptors with ORB
kp, des = orb.compute(img, kp)
# print kp
for i in kp:
	print i.pt
# end = time.clock()

# print "%.2gs" % (end-start)


# print kp

# draw only keypoints location,not size and orientation
img2 = cv2.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)

plt.imshow(img2), plt.show()