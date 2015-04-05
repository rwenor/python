import io
import picamera

my_s = io.BytesIO()

camera = picamera.PiCamera()
#camera.vflip = True
#camera.hflip = True
camera.resolution = (640, 480)

for i in range(1, 11):
    camera.capture(my_s, 'jpeg')
    print i
    
