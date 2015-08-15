import io
import time
import picamera

import multiprocessing

img = []



def img_load(img_q, stream, i):

    img = Image.open(stream)
    #q.task_done()
    
    buffer = img.load()
    dprt('Loaded ' + str( i ) )
    queue2.put(i)
    
    
    if buf1 is None:
        dprt('Buff setup')
        #buf0 = buffer
        buf1 = buffer
        #img0 = img
        img1 = img
            
    
    changedPixels0, takePicture0, debugimage = GetDiffDbImg(buf1, buffer)
    #dprt('Moved' + str(takePicture0))
    if takePicture0:
        saveImage2(img, diskSpaceToReserve, i)
        
    
    buf1 = buffer
    img1 = img    
    dprt('Ut ' + str( i ) )

    
    return stream

def img_worker(q, q2, stream,i, sem):
    #print 'img_w'

    stream = q.get()
    i = -1

    while (stream <> None):
        i += 1

        #print "Wrk:", i
        stream.seek(0)
        #time.sleep(0.0)
        q2.put(stream)
        
        stream = q.get()

    print "Wrk end"
    

def empyt_q2(q, q2, stream,i, sem):
    #print 'img_w'

    stream = q2.get()
    i = -1

    while (stream <> None):
        i += 1

        print "Que:", i
        stream.seek(0)
        
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
    queue.put(None)
    
        
    

with picamera.PiCamera() as camera:
    queue = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()

    for i in range(0,4):
        queue2.put( io.BytesIO() )

    print queue2
    #queue.put(None)

    tw = multiprocessing.Process(name='worker 1', target=img_worker, args=(queue, queue2, None,0, None))
    ##tw = threading.Thread(target=img_worker, args=(queue, queue2, None,0, None))
    tw.start()
    
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
 
    #time.sleep(1)
    #queue.put(None)

    print "-"
    #if tw.is_alive():
    #    tw.join()
    print "="
    queue2.put(None)


    tw = multiprocessing.Process(name='empty q2', target=empyt_q2, args=(queue, queue2, None,0, None))
    ##tw = threading.Thread(target=img_worker, args=(queue, queue2, None,0, None))
    tw.start()
    tw.join()

    #while queue2.get() <> None:
    #    print "*"

        
    print queue

