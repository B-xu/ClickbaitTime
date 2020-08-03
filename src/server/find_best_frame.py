# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 22:39:41 2020

@author: xy
"""

import cv2 as cv
import time
import urllib.request as urllib
import numpy as np

start = time.time() #start timing

#load files/video
url = 'https://i.ytimg.com/vi/MnNLTKa-VFw/mqdefault.jpg'
resp = urllib.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype="uint8")
gray = cv.imdecode(image, cv.IMREAD_GRAYSCALE)
video_path = 'https://r4---sn-nx5e6ne6.googlevideo.com/videoplayback?expire=1596499619&ei=Q1IoX461BcmagQen06yoAw&ip=136.243.55.47&id=o-AFWpbJVIhb9mSOuR7jxLTzMx6CSrkgFhi2Kw9VqZcD5g&itag=160&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278%2C394%2C395%2C396%2C397%2C398%2C399&source=youtube&requiressl=yes&vprv=1&mime=video%2Fmp4&gir=yes&clen=7813448&dur=756.920&lmt=1575374040081048&fvip=4&keepalive=yes&fexp=23812954,23883098&c=WEB&txp=5535432&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgSr1X4PgGZRELlk3dlDKgJKJYEZnE01oWKFnwdsGsluECIQDVmG7EDw2Y8hvtFJXtZAfLA1ALaZWGB_GmLHrNZHt5NA%3D%3D&ratebypass=yes&rm=sn-4g5e6r7z&req_id=ae8e7166b5c7a3ee&redirect_counter=2&cm2rm=sn-ni5f-t8gs7z&cms_redirect=yes&ipbypass=yes&mh=pI&mip=24.86.140.150&mm=30&mn=sn-nx5e6ne6&ms=nxu&mt=1596477918&mv=m&mvi=4&pl=22&lsparams=ipbypass,mh,mip,mm,mn,ms,mv,mvi,pl&lsig=AG3C_xAwRAIgfE1faN-pSp0-yrF3DEWSXse8PD72vHfAUVkGq06ZIaoCIDsypPtdcLGZx0uK8rcJYTSWHaByJchs03mk08Eut-aA'
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


