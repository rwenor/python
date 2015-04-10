import io
import time
import picamera
from PIL import Image
import threading
import logging

deb_time = time.time()

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

# Test-Image settings
testWidth = 640
testHeight = 480

def dprt(dstr):
    diff = time.time() - deb_time
    logging.debug(str(diff) + ': ' + dstr)

def img_load(stream,i):
    img = Image.open(stream)
    buffer = img.load()
    if i == 0:
        buf0 = buffer
        buf1 = buf0
            

    dprt('Loaded')


def outputs():
    stream = io.BytesIO()
    for i in range(40):
        # This returns the stream for the camera to capture to
        yield stream
        # Once the capture is complete, the loop continues here
        # (read up on generator functions in Python to understand
        # the yield statement). Here you could do some processing
        # on the image...
        stream.seek(0)
        
        dprt(str(i))


        t = threading.Thread(target=img_load, args=(stream,i,))
        t.start()
        time.sleep(0.0001) # let tread start...
        
        # Finally, reset the stream for the next capture
        stream.seek(0)
        stream.truncate()

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 80
    time.sleep(2)
    start = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
    print('Captured 40 images at %.2ffps' % (40 / (finish - start)))
    
