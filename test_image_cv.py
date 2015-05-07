
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def p(str):
    print str
    
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)

rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.1)

for i in range(2):  #virket ikke
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
     
    # display the image on screen and wait for a keypress
    cv2.imshow("Image", image)
    #rawCapture = PiRGBArray(camera)

    p('i: '+ str(i))
    cv2.waitKey(0)
    
print 'wk'
cv2.waitKey(0)
p('end')
