import io
import time
import picamera
import multiprocessing
import threading
import logging
from PIL import Image

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s', )

def slow_worker():
    logging.debug('Starting worker')
    time.sleep(0.1)
    logging.debug('Finished worker')
            

if __name__ == '__main__':
    # p = multiprocessing.Process(target=slow_worker)
    p = threading.Thread(target=slow_worker)
    print('BEFORE:', p, p.is_alive())
    
    p.start()
    time.sleep(5)
    print 'DURING:', p, p.is_alive()
    
    #p.terminate()
    print 'TERMINATED:', p, p.is_alive()

    p.join()
    print 'JOINED:', p, p.is_alive()



def do_capture():
    for i in range(40):
        print i
        time.sleep(0.5)

# Set up 40 in-memory streams
outputs = [io.BytesIO() for i in range(40)]
    
def do_capturex():
    with picamera.PiCamera() as camera:
        # Set the camera's resolution to VGA @40fps and give it a couple
        # of seconds to measure exposure etc.
        camera.resolution = (640, 480)
        camera.framerate = 4
        print 'In capt'
        time.sleep(2)
        
        start = time.time()
        camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
        finish = time.time()
        # How fast were we?
        print('Captured 40 images at %.2ffps' % (40 / (finish - start)))

def open_img(imageData):
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer

if __name__ == '__main__':
    c = threading.Thread(name='co_camCapt', target=do_capturex)
    c.start()

    for i in range(40):
        print i, outputs[i].__sizeof__()
        #image2, buffer2 = open_img(outputs[i])
        time.sleep(1)
        
    c.join
