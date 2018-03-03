# from threading import Thread, Condition
# import time
# import random
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt


# cap = cv2.VideoCapture('test.mp4')

# if (cap.isOpened()== False): 
#   print("Error opening video stream or file")

# queue = []
# MAX_NUM = 500
# condition = Condition()
# orb = cv2.ORB_create()



# class ProducerThread(Thread):
#     def run(self):
#         global queue
#         while True:
#             condition.acquire()
#             if len(queue) == MAX_NUM:
#                 condition.wait()  
#             if (cap.isOpened()):
#                 ret, frame = cap.read()
#                 if ret == True:
#                     queue.append(frame)
#                 if cv2.waitKey(25) & 0xFF == ord('q'):
#                     break
#             else:
#                 print "No more footage"
#                 condition.notify()
#                 condition.release()
#                 break
#             if (cap.isOpened()):
#                 ret, frame = cap.read()
#                 if ret == True:
#                     queue.append(frame)
#                 if cv2.waitKey(25) & 0xFF == ord('q'):
#                     break
#             else:
#                 print "No more footage"
#                 condition.notify()
#                 condition.release()
#                 break
#             condition.notify()
#             condition.release()
#             time.sleep(random.random())


# class ConsumerThread(Thread):
#     def run(self):
#         global queue
#         while True:
#             condition.acquire()
#             if not queue:
#                 print "Nothing in queue, consumer is waiting"
#                 condition.wait()
#                 print "Producer added something to queue and notified the consumer"
#             img1 = queue.pop(0)  # queryImage
#             img2 = queue.pop(0)  # trainImage

#             upper_half = np.hsplit(np.vsplit(img1, 2)[0], 2)
#             lower_half = np.hsplit(np.vsplit(img1, 2)[1], 2)

#             upper_left = upper_half[0]
#             upper_right = upper_half[1]
#             lower_left = lower_half[0]
#             lower_right = lower_half[1]

#             upper_half2 = np.hsplit(np.vsplit(img2, 2)[0], 2)
#             lower_half2 = np.hsplit(np.vsplit(img2, 2)[1], 2)

#             upper_left2 = upper_half2[0]
#             upper_right2 = upper_half2[1]
#             lower_left2 = lower_half2[0]
#             lower_right2 = lower_half2[1]

#             temp = [[upper_left, upper_left2], [upper_right,upper_right2], [lower_left,lower_left2], [lower_right, lower_right2]]
#             for i in range(len(temp)):
#                 img1 = temp[i][0]
#                 img2 = temp[i][1]
#                 kp1, des1 = orb.detectAndCompute(img1,None)
#                 kp2, des2 = orb.detectAndCompute(img2,None)
#                 bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#                 matches = bf.match(des1,des2)
#                 matches = sorted(matches, key = lambda x:x.distance)
#                 print "Consumed", sum(int(i.distance) for i in matches)
#             print
#             condition.notify()
#             condition.release()
#             time.sleep(random.random())


# ProducerThread().start()
# ConsumerThread().start()
from threading import Thread, Condition
import time
import random
import cv2
import numpy as np
from matplotlib import pyplot as plt


cap = cv2.VideoCapture('test.mp4')

if (cap.isOpened()== False): 
  print("Error opening video stream or file")

queue = []
MAX_NUM = 500
condition = Condition()
orb = cv2.ORB_create()



class ProducerThread(Thread):
    def run(self):
        global queue
        while True:
            condition.acquire()
            if len(queue) == MAX_NUM:
                condition.wait()  
            if (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    queue.append(frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                print "No more footage"
                condition.notify()
                condition.release()
                break
            if (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    
                    queue.append(frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                print "No more footage"
                condition.notify()
                condition.release()
                break
            condition.notify()
            condition.release()
            time.sleep(random.random())


class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            condition.acquire()
            if not queue:
                print "Nothing in queue, consumer is waiting"
                condition.wait()
                print "Producer added something to queue and notified the consumer"
            img1 = queue.pop(0)  # queryImage
            img2 = queue.pop(0)  # trainImage

            hsplit1 = np.hsplit(img1, 2)
            hsplit2 = np.hsplit(img2, 2)
            split1 = []
            split2 = []
            for i in range(len(hsplit1)):
                temp1 = np.vsplit(hsplit1[i], 2)
                # print temp1[0].size
                temp2 = np.vsplit(hsplit2[i], 2)
                for i in range(len(temp1)):
                    split1.append(temp1[i])
                    split2.append(temp2[i])
                # split.append([np.vsplit(hsplit1[i], 8), np.vsplit(hsplit2[i], 8)])



            # temp = [[upper_left, upper_left2], [upper_right,upper_right2], [lower_left,lower_left2], [lower_right, lower_right2]]
            for i in range(len(split1)):
                img11 = split1[i]
                img22 = split2[i]
                print type(img1)
                print i
                print img1.size
                print img2.size
                kp1, des1 = orb.detectAndCompute(img11,None)
                kp2, des2 = orb.detectAndCompute(img22,None)
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1,des2)
                matches = sorted(matches, key = lambda x:x.distance)
                print "Consumed", sum(int(i.distance) for i in matches)
                print
            print
            condition.notify()
            condition.release()
            time.sleep(random.random())


ProducerThread().start()
ConsumerThread().start()