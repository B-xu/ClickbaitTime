import cv2 as cv
import numpy as np
import urllib.request as urllib

url = 'https://i.ytimg.com/vi/Z996j8DKaOw/mqdefault.jpg'
video_path = 'https://r3---sn-p5qs7nek.googlevideo.com/videoplayback?expire=1596794034&ei=UtAsX831KqCE6dsPnMypqAQ&ip=136.243.55.47&id=o-AIYo9uf6FtWiIdAxsFXC4ZYY49Hel4qKNtYDTxbsn1d1&itag=160&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278%2C394%2C395%2C396%2C397%2C398%2C399&source=youtube&requiressl=yes&vprv=1&mime=video%2Fmp4&gir=yes&clen=6037629&dur=601.120&lmt=1575764987635758&fvip=3&keepalive=yes&fexp=23812954,23883098&c=WEB&txp=6535432&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRAIgKjQ8AYOowHaRQNHffqKvPjZveYYcG9tbBAsbNOO0H48CIDNJtaliCWmzavxjf4JuI-svc515GYGU88-0u-2QMnSV&ratebypass=yes&redirect_counter=1&rm=sn-4g5els7s&req_id=2227939e9c59a3ee&cms_redirect=yes&ipbypass=yes&mh=Hy&mip=207.81.167.8&mm=31&mn=sn-p5qs7nek&ms=au&mt=1596772278&mv=D&mvi=3&pl=0&lsparams=ipbypass,mh,mip,mm,mn,ms,mv,mvi,pl&lsig=AG3C_xAwRgIhAMVny-eMHk9zvhEervJtAorV0qUC87O2scZKKrROoJ3hAiEA-S2tz4FxkYHmZoep4uJkgCxz1M-Rc2UMFDjXX3XTEVo%3D'

def find_frame(url, video_path):
    
    #load the image from URL
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    gray = cv.imdecode(image, cv.IMREAD_GRAYSCALE)
    
    bf = cv.BFMatcher() #feature matching object
    #sift = cv.xfeatures2d.SIFT_create() #sift detection object
    sift = cv.SIFT_create()
    kp, des = sift.detectAndCompute(gray,None) #get keypoints of thumbnail
    
    
    #get videocapture from video URL
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
            for match in matches: #ratio test
                if len((match)) < 2:
                    continue
                m,n = match
                if m.distance < 0.75*n.distance:
                    good += 1
                    
            if good > best_match:
                best_match = good
                #best_img = img
                best_fno = fno
    
        fno += 1
        success = cap.grab()
    
    cap.release()
    
    if (best_match/len(kp) < 0.1): #no match condition
        print("NO MATCH")
    
    minutes = int((best_fno/sample_rate_exact)//60)
    seconds = round((best_fno/sample_rate_exact)%60)
    
    return("%d:%02d" % (minutes,seconds)) #time stamp
