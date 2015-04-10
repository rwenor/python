import io
import time
import picamera
from datetime import datetime, timedelta

def wait():
    # Calculate the delay to the start of the next hour
    #next_hour = (datetime.now() + timedelta(hour=1)).replace(
    #    minute=0, second=0, microsecond=0)
    #delay = (next_hour - datetime.now()).seconds
    time.sleep(0.5)

img_s = io.BytesIO()
with picamera.PiCamera() as camera:
    #camera.start_preview()
    wait()
    for filename in camera.capture_continuous(img_s, 'bmp'):
        print('Captured %s' % filename)
        #wait()
