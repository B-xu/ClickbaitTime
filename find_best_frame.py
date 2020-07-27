# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 22:39:41 2020

@author: xy
"""

import cv2 as cv
import time


gray = cv.imread('C:\\Users\\xy\\Documents\\thumb1.jpg', cv.IMREAD_GRAYSCALE)
video_path = 'C:\\Users\\xy\\Downloads\\videoplayback-1.mp4'
height, width = gray.shape

orb = cv.ORB_create()
kp, des = orb.detectAndCompute(gray,None)

bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

cap = cv.VideoCapture(video_path)
sample_rate = 24

start1 = time.time()
sift = cv.xfeatures2d.SIFT_create()
kp, des = sift.detectAndCompute(gray,None)
end1 = time.time()

#
print(len(kp))
print(end1-start1)

cap = cv.VideoCapture(video_path)
#sample_rate = 30
sample_rate = 24
success = cap.grab() # get the next frame
fno = 0
best_match = 0
start = time.time()
while success:
    if fno % (sample_rate) == 0:
        _, img = cap.retrieve()
		#do_something(img)
        #print(fno)
        #cv2.imshow(str(fno),img)
        #cv2.waitKey(0)
        cmp = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        #cmp = cv.resize(cmp, (960,540))
        #cmp = cv.resize(cmp, (width,height))
        kp1, des1 = sift.detectAndCompute(cmp,None)
        
        try:
            matches = bf.knnMatch(des,des1,k=2)
        except:
            matches = []
        
        good = 0
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good += 1
                
        if good > best_match:
            best_match = good
            best_img = img
            	# read next frame
        #print(fno, "of 9000")
    fno += 1
    success = cap.grab()

end = time.time()
print(end-start)
cv.imwrite('best_match_orb.jpg',best_img)