# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 22:39:41 2020

@author: xy
"""

import cv2 as cv
import time

start = time.time() #start timing

#load files/video
gray = cv.imread('C:\\Users\\xy\\Documents\\thumb2.jpg', cv.IMREAD_GRAYSCALE)
video_path = 'C:\\Users\\xy\\Downloads\\videoplayback-5.mp4'

bf = cv.BFMatcher() #feature matching object

sift = cv.xfeatures2d.SIFT_create() #sift detection object
kp, des = sift.detectAndCompute(gray,None) #get keypoints of thumbnail

cap = cv.VideoCapture(video_path) #get video
sample_rate_exact = cap.get(cv.CAP_PROP_FPS) #find frame rate 
sample_rate = round(sample_rate_exact) #rounded frame rate (for while loop)
success = cap.grab() # get the next frame
fno = 0 #frame number
best_match = 0 #maximum number of matches
best_fno = 0 #frame number of closes match

while success:
    if fno % (sample_rate) == 0: #sample rate of about 1 frame per second
        _, img = cap.retrieve()
        cmp = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        kp1, des1 = sift.detectAndCompute(cmp,None)
        
        try:
            matches = bf.knnMatch(des,des1,k=2)
        except:
            matches = []
        
        good = 0
        for m,n in matches: #ratio test
            if m.distance < 0.75*n.distance:
                good += 1
                
        if good > best_match:
            best_match = good
            best_img = img
            best_fno = fno

    fno += 1
    success = cap.grab()

end = time.time()
cap.release()
print('Run Time:',end-start)

if (best_match/len(kp) < 0.1): #no match condition
    print("NO MATCH")

minutes = int((best_fno/sample_rate_exact)//60)
seconds = round((best_fno/sample_rate_exact)%60)

print(str(minutes)+':'+str(seconds)) #time stamp

cv.imshow('best match',best_img)
cv.imshow('original image', gray)
cv.waitKey(0)
cv.destroyAllWindows()


