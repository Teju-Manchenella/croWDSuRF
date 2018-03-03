import numpy as np
import cv2
from matplotlib import pyplot as plt
import time


img1 = cv2.imread('welch1.png',0)          # queryImage
img2 = cv2.imread('welch2.png',0) # trainImage

# Initiate SIFT detector
orb = cv2.ORB_create()

upper_half = np.hsplit(np.vsplit(img1, 2)[0], 2)
lower_half = np.hsplit(np.vsplit(img1, 2)[1], 2)

upper_left = upper_half[0]
upper_right = upper_half[1]
lower_left = lower_half[0]
lower_right = lower_half[1]

upper_half2 = np.hsplit(np.vsplit(img2, 2)[0], 2)
lower_half2 = np.hsplit(np.vsplit(img2, 2)[1], 2)

upper_left2 = upper_half2[0]
upper_right2 = upper_half2[1]
lower_left2 = lower_half2[0]
lower_right2 = lower_half2[1]

temp = [[upper_left, upper_left2], [upper_right,upper_right2], [lower_left,lower_left2], [lower_right, lower_right2]]
plt.imshow(temp[0][1]), plt.show()
# plt.imshow(temp[0][1]), plt.show()
for i in range(len(temp)):
	img1 = temp[i][0]
	
	img2 = temp[i][1]
	kp1, des1 = orb.detectAndCompute(img1,None)
	kp2, des2 = orb.detectAndCompute(img2,None)
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	matches = bf.match(des1,des2)

	matches = sorted(matches, key = lambda x:x.distance)
	print "Consumed", sum(int(i.distance) for i in matches)

    # print "Consumed", sum(int(i.distance) for i in matches)
# for i in matches:
# 	print i.distance
# 	print i.imgIdx
# 	print kp1[i.queryIdx].pt
# 	print kp2[i.trainIdx].pt
# 	print

# for i in range(len(matches)):
# 	print kp1[matches[i].queryIdx].pt
# 	print kp2[matches[i].queryIdx].pt
# 	print

# Draw first 10 matches.
# img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches, None, flags=2)

# plt.imshow(img3),plt.show()