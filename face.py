import numpy as np
import cv2
import os
import time
import subprocess 
# from goto import with_goto
# label .begin
start_time = time.time()
t_end = time.time() + 10
def thread1():
    os.chdir("/home/pi/opencv-3.3.0/data/haarcascades")
    #capture_duration = 5
    face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)
    while time.time() < t_end:
    
        ret, img = cap.read()
        img = cv2.flip(img,-1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
        #print "Face Detected"
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                cap.release()
                cv2.destroyAllWindows()
                python_bin = "/home/pi/Desktop/azure-faceApi/faceEnv/bin/python"
                script_file = "/home/pi/Desktop/azure-faceApi/aks.py"
                subprocess.Popen([python_bin, script_file])
                                                
        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


    python_bin = "/home/pi/Desktop/azure-faceApi/faceEnv/bin/python"
    script_file = "/home/pi/Desktop/azure-faceApi/aks.py"
    subprocess.Popen([python_bin, script_file])

thread1()