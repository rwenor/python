import io
import time
import picamera

img = []

def outputs():
    
    for i in xrange(0, 40):
        stream = io.BytesIO()
        yield stream
        print i
        time.sleep(0.08)
        stream.seek(0)
        img.append(stream)

        
    

with picamera.PiCamera() as camera:
    # Set the camera's resolution to VGA @40fps and give it a couple
    # of seconds to measure exposure etc.
    camera.resolution = (640, 480)
    camera.framerate = 80
    time.sleep(2)
    # Set up 40 in-memory streams
    #outputs = [io.BytesIO() for i in range(40)]
    start = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
    # How fast were we?
    print('Captured 40 images at %.2ffps' % (40 / (finish - start)))

    print img

