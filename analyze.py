from threading import Thread, Condition
import time
import random
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image 


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
                    print frame.size
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                print "No more footage"
                condition.notify()
                condition.release()
                break
            ret, frame = cap.read()
            ret, frame = cap.read()
            ret, frame = cap.read()
            ret, frame = cap.read()
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

           
            hsplit1 = np.hsplit(img1, 8)
            hsplit2 = np.hsplit(img2, 8)
            split1 = []
            split2 = []
            for i in range(len(hsplit1)):
                temp1 = np.vsplit(hsplit1[i], 8)
                # print temp1[0].size
                temp2 = np.vsplit(hsplit2[i], 8)
                for i in range(len(temp1)):
                    split1.append(temp1[i])
                    split2.append(temp2[i])
            final = []
            f = open('output.txt', 'w')
            iIter = 0
            for i in range(len(split1)):
             	img1= split1[i]
                img2 = split2[i]
                metric = np.sum(np.absolute(img2 - img1))
            	
                final.append(metric)
                # print metric
                # kp1, des1 = orb.detectAndCompute(img1,None)
                # kp2, des2 = orb.detectAndCompute(img2,None)
                # if des1 is None:
                # 	print "des1"
                	
                # elif des2 is None:
                # 	print "des2"
                # else:
	               #  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	               #  matches = bf.match(des1,des2)
	               #  matches = sorted(matches, key = lambda x:x.distance)
	               #  print "Consumed", sum(int(i.distance) for i in matches)
            output = np.array(final).reshape((8,8))
            np.savetxt("visualizer1/foo.csv", output, delimiter=",")
            condition.notify()
            condition.release()
            time.sleep(random.random())


ProducerThread().start()
ConsumerThread().start()