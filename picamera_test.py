import time
import picamera

# Explicitly open a new file called my_image.jpg
my_file = open('my_image.jpg', 'wb')
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture(my_file)
# At this point my_file.flush() has been called, but the file has
# not yet been closed
my_file.close()
