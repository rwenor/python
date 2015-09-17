import io
import time
import picamera
from PIL import Image

import logging
import multiprocessing

img = []

workerList = []

# debugPrint - Using logging
deb_time = time.time()
no_deb = False

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
def dprt(dstr, f = False):
    if no_deb and not f:
        return

    diff = int((time.time() - deb_time)*1000)
    logging.debug(str(diff) + ': ' + dstr)



def img_load(img_q, stream, i):

    img = Image.open(stream)
    #q.task_done()
    
    buf = img.load()
    dprt('Loaded ' + str( i ) )
    img_q.put(buf)
    
    
    #changedPixels0, takePicture0, debugimage = GetDiffDbImg(buf1, buffer)
    #dprt('Moved' + str(takePicture0))
    #if takePicture0:
    #    saveImage2(img, diskSpaceToReserve, i)
          
    dprt('Ut ' + str( i ) )
    return buf


def img_worker(q, q2, img_q, i, sem):
    #print 'img_w'

    stream = q.get()
    i = -1

    while (stream <> None):
        i += 1

        dprt( "Wrk:" +  str(i) )
        stream.seek(0)
        img_load(img_q, stream, i)

        # Done with stream
        stream.seek(0)
        q2.put(stream)
        
        stream = q.get()

    print "Wrk end"
    

def empyt_q(q2):
    #print 'img_w'

    stream = q2.get()
    i = -1

    while (stream <> None):
        i += 1

        print "Que:", i
        #stream.seek(0)
        
        stream = q2.get()

    print "Que end"


def outputs(queue, queue2):
    
    for i in xrange(0, 40):
        stream = queue2.get()
        yield stream
        print "Cap:", i
        #time.sleep(0.08)
        queue.put(stream)

    print "Output end"
    for w in workerList:
        queue.put(None)
    
        
    

with picamera.PiCamera() as camera:
    queue = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    img_q = multiprocessing.Queue()

    for i in range(0,4):
        queue2.put( io.BytesIO() )

    print queue2
    #queue.put(None)
    for i in range(2):
        tw = multiprocessing.Process(name='worker', target=img_worker, args=(queue, queue2, img_q,0, None))
        tw.start()
        workerList.append(tw)

    # Set the camera's resolution to VGA @40fps and give it a couple
    # of seconds to measure exposure etc.
    camera.resolution = (640, 480)
    camera.framerate = 80
    time.sleep(2)
    # Set up 40 in-memory streams
    #outputs = [io.BytesIO() for i in range(40)]
    start = time.time()
    camera.capture_sequence(outputs(queue, queue2), 'jpeg', use_video_port=True)
    finish = time.time()
    # How fast were we?
    print('Captured 40 images at %.2ffps' % (40 / (finish - start)))
 
    time.sleep(2)
    #queue.put(None)

    print "-"
    #if tw.is_alive():
        #tw.join()
    print "="
    queue2.put(None)
    img_q.put(None)


    tw = multiprocessing.Process(name='empty q2', target=empyt_q, args=(queue2,))
    tw.start()
    tw = multiprocessing.Process(name='empty img_q', target=empyt_q, args=(img_q,))
    tw.start()
    #tw.join()

    #while queue2.get() <> None:
    #    print "*"

        
    print queue

