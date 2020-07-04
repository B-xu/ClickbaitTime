# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 12:29:51 2020

@author: xy
"""

import cv2
video_path = 'D:\\DCIM\\1\\VID_157.MOV'
cap = cv2.VideoCapture(video_path)
sample_rate = 30
success = cap.grab() # get the next frame
fno = 0
while success:
    if fno % (sample_rate*10) == 0:
        _, img = cap.retrieve()
		#do_something(img)
        #print(fno)
        cv2.imshow(str(fno),img)
        cv2.waitKey(0)
	# read next frame
    fno += 1
    success = cap.grab()