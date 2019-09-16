'''
Name: face_tracker_picam.py
James Tregaskis
Aug 2019
This uses openncv to detect a face (front view and eyes)
using haarcascade_frontalface_default.xml and haarcascade_eye.xml
The detected face is rendered with text relating to
ther surveillance theme of this installed piece.
'''
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import random

#point to the haar cascade file in the directory
facesXmlFile = "haarcascade_frontalface_default.xml"
eyesXmlFile = "haarcascade_eye.xml"

faceCascade = cv2.CascadeClassifier(facesXmlFile)
eyesCascade = cv2.CascadeClassifier(eyesXmlFile)

#starting camera
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
camera.rotation = 180
camera.hflip = 180
camera.vflip = 0

rawCapture = PiRGBArray(camera, size=(320, 240))
mylabel=""
time.sleep(0.2)

for snapshot in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	'''
	capture the frame in an array,
	converted into black and whiteto simplify processing
	'''
	image = snapshot.array
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	mugshots = faceCascade.detectMultiScale(
		image,
		scaleFactor = 1.1,
		minNeighbors = 5,
		minSize=(30, 30),
		flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)
	'''
	rectangle drawn around the face
	(and eyes, if eyes are picked up).
	'''
	for(x,y,w,h) in mugshots:
		cv2.putText(img=image, text=mylabel, org=(x, y-4), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.15*3, color=(255,255,255))
		cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,255),2)
		roi_gray =gray[y:y+h, x:x+w]
		roi_color = image[y:y+h, x:x+w]
		eyes = eyesCascade.detectMultiScale(roi_gray)
		for (ex, ey,ew,eh) in eyes:
			cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255,255,255), 2)
	cv2.namedWindow("Display", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("Display",cv2.WND_PROP_FULLSCREEN,1)
	mylabel = random.choice(["criminal","gullible customer","big spender", "vip","on watch list", "terrorist", "sex offender", "known paedophile" , "shoplifter", "political suspect", "troublemaker"])
	#display image
	cv2.imshow("Display", image)
	'''
	stream capture cleared down
	'''
	rawCapture.truncate(0)
