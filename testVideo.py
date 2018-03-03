import cv2
import numpy as np
from matplotlib import pyplot as plt


cap = cv2.VideoCapture('test.mp4')

if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# orb = cv2.ORB_create()
temp = []


while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    temp.append(frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  else: 
    break
 
cap.release()
 
# Closes all the frames
# cv2.destroyAllWindows()
print len(temp)
orb = cv2.ORB_create()

for i in range(1,len(temp)):
img1 = temp[i-1]
img2 = temp[i]  

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
for i in range(len(temp)):
    img1 = temp[i][0]
    img2 = temp[i][1]
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1,des2)
    matches = sorted(matches, key = lambda x:x.distance)
    print "Consumed", sum(int(i.distance) for i in matches)
print

# # Initiate SIFT detector

# # find the keypoints and descriptors with ORB
# kp1, des1 = orb.detectAndCompute(img1,None)
# kp2, des2 = orb.detectAndCompute(img2,None)

# # print des1
# # create BFMatcher object
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# # print bf
# # Match descriptors.
# matches = bf.match(des1,des2)

# # Sort them in the order of their distance.
# matches = sorted(matches, key = lambda x:x.distance)
# img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], None, flags=2)
# plt.imshow(img3),plt.show()