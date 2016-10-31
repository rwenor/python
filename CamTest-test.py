import time
import picamera

//test test Test create
// Edit by rolf

with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(1)

    camera.hflip = True
    camera.vflip = True

    camera.capture('/var/www//image.jpg')
    camera.stop_preview()
