import io
import os
import time
import picamera
from PIL import Image
import threading
import logging
import multiprocessing
from datetime import datetime
#import getch
import pygame

def getch():
  import sys, tty, termios
  old_settings = termios.tcgetattr(0)
  new_settings = old_settings[:]
  new_settings[3] &= ~termios.ICANON
  try:
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(0, termios.TCSANOW, old_settings)
  return ch


no_deb = False #True

# printTimeDiff
PrintTimeDiffLast = time.time()
PrintTimeCnt = 0

def PTD(str, f = False):
    if no_deb and not f:
        return
    global PrintTimeDiffLast
    global PrintTimeCnt
    logging.debug('PTD%4s: %6s - %s' %  (PrintTimeCnt, \
                               int((time.time() - PrintTimeDiffLast)*1000), \
                               str) \
                  )
    
    PrintTimeCnt += 1
    PrintTimeDiffLast = time.time()



# debugPrint - Using logging
deb_time = time.time()
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
def dprt(dstr, f = False):
    if no_deb and not f:
        return

    diff = int((time.time() - deb_time)*1000)
    logging.debug(str(diff) + ': ' + dstr)



# Test-Image settings
imgCnt = 50
testWidth = 640
testHeight = 480
filepath = "/var/www/picam"
filenamePrefix = "cap"

debugMode = True       # False or True
testAreaCount = 1
testBorders = [ [[1,testWidth],[1,testHeight]] ]  # [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
threshold = 20     # 10 diff
sensitivity = 30   # 20 cnt

do_quit = False

# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du


# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".jpg"):
                os.remove(filepath + "/" + filename)
                print "Deleted %s/%s to avoid filling disk" % (filepath,filename)
                if (getFreeSpace() > bytesToReserve):
                    return


# Beregnerer diff og gir debug bilde
def GetDiffDbImg(buffer1, buffer2):
    PTD('GetDiffDbImg')
    takePicture = False
    # Count changed pixels
    changedPixels = 0
    cp5 = 0
    cp10 = 0
    cp15 = 0
    maxDiff =  0

    if (debugMode): # in debug mode, save a bitmap-file with marked changed pixels and with visible testarea-borders
        debugimage = Image.new("RGB",((testWidth >> 3) + 1, (testHeight >> 3) + 1))
        #print 'TestImg: %s, %s' % (((testWidth >> 3) + 1, (testHeight >> 3) + 1))
        debugim = debugimage.load()

    for z in xrange(0, testAreaCount): # = xrange(0,1) with default-values = z will only have the value of 0 = only one scan-area = whole picture
        for x in xrange(testBorders[z][0][0]-1, testBorders[z][0][1], 8): # = xrange(0,100) with default-values
            for y in xrange(testBorders[z][1][0]-1, testBorders[z][1][1], 8):   # = xrange(0,75) with default-values; testBorders are NOT zero-based, buffer1[x,y] are zero-based (0,0 is top left of image, testWidth-1,testHeight-1 is botton right)

                if (debugMode):
                    #print '%s, %s > %s, %s' % (x, y, x >> 3, y >> 3) 
                    debugim[x >> 3, y >> 3] = buffer2[x,y]
                    if ((x == testBorders[z][0][0]-1) or (x == testBorders[z][0][1]-1) or (y == testBorders[z][1][0]-1) or (y == testBorders[z][1][1]-1)):
                        # print "Border %s %s" % (x,y)
                        debugim[x >> 8, y >> 8] = (0, 0, 255) # in debug mode, mark all border pixel to blue


                # Just check green channel as it's the highest quality channel
                pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
                #if pixdiff > 0:
                #    print pix

                if pixdiff > maxDiff:
                    maxDiff = pixdiff
                        
                if pixdiff > threshold:
                    changedPixels += 1
                if pixdiff > 5:
                    cp5 += 1
                if pixdiff > 10:
                    cp10 += 1
                if pixdiff > 15:
                    cp15 += 1
                    
                    if (debugMode):
                        debugim[x >> 3,y >> 3] = (buffer2[x,y][0], buffer2[x,y][1] + pixdiff << 1, buffer2[x,y][2]) # in debug mode, mark all changed pixel to green
                else:
                    if ((debugMode) and (pixdiff > 2)):
                        debugim[x >> 3,y >> 3] = (buffer2[x,y][0], (buffer2[x,y][1] >> 0) + (pixdiff << 1), buffer2[x,y][2]) # in debug mode, mark all changed pixel to green
                


                # Save an image if pixels changed
                if (changedPixels > sensitivity):
                    takePicture = True # will shoot the photo later
                if ((debugMode == False) and (changedPixels > sensitivity)):
                    break  # break the y loop
                
            if ((debugMode == False) and (changedPixels > sensitivity)):
                break  # break the x loop
            
        if ((debugMode == False) and (changedPixels > sensitivity)):
            break  # break the z loop
    
    PTD('End')
    dprt( "Change: %s changed pixel, maxDiff = %s, 5 = %s 10 = %s, 15 = %s" % (changedPixels, maxDiff, cp5, cp10, cp15))
    
    if (debugMode):
        return changedPixels, takePicture, debugimage
    else:
        return changedPixels, takePicture, 0

diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
buf0 = None
buf1 = None


# Save a full size image to disk
def saveImage2(image2, diskSpaceToReserve, imgNr):
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = filepath + "/" + filenamePrefix + "-%04d%02d%02d-%02d%02d%02d-%04d.jpg" \
               % (time.year, time.month, time.day, time.hour, time.minute, time.second, imgNr)
    #subprocess.call("raspistill %s -w %s -h %s -t 200 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), shell=True)
    image2.save(filename) # save debug image as bmp
    dprt( "Captured %s" % filename )
    

def img_load(q, stream,i):
    global buf0
    global buf1

    dprt('Inn ' + str( 1 + (i % 2)) )

##    print "stream = ", stream
    stream = q.get()
##    print "stream ?= ", stream

    img = Image.open(stream)
    #q.task_done()
    
    buffer = img.load()
    if i == 0:
        buf0 = buffer
        buf1 = buffer
        img0 = img
        img1 = img
            
    dprt('loaded ')
    changedPixels0, takePicture0, debugimage = GetDiffDbImg(buf1, buffer)
    #dprt('Moved' + str(takePicture0))
    if takePicture0:
        saveImage2(img, diskSpaceToReserve, i)
        
    
    buf1 = buffer
    img1 = img    
    dprt('Ut ' + str( 1 + (i % 2)) ) 


def outputs():
    global do_quit

    stream1 = io.BytesIO()
    stream2 = io.BytesIO()
    stream = stream2

#    i = 0
    for i in range(imgCnt):
    #while i <> imgCnt:
    #    i += 1
        stream = io.BytesIO()
                           
        # This returns the stream for the camera to capture to
        PTD('Capt ' + str(i), True)
        yield stream

        PTD('Prep')
        # Once the capture is complete, the loop continues here
        # (read up on generator functions in Python to understand
        # the yield statement). Here you could do some processing
        # on the image...
        stream.seek(0)
        
        #dprt(str(i))
        #time.sleep(0.001) # let tread stop...

        queue.put(stream)
        t = threading.Thread(target=img_load, args=(queue, stream,i,))
        #t = multiprocessing.Process(target=img_load, args=(stream,i,))
        t.start()
        time.sleep(0.001) # let tread start...
        
        # Finally, reset the stream for the next capture
##        if i % 2:
##            stream = stream1
##            PTD('Stream1 reset')
##        else:
##            stream = stream2
##            PTD('Stream2 reset')
##            
##        stream.seek(0)
##        stream.truncate()

        if do_quit:
            break
          
    do_quit = True


def keyLoop():
    global do_quit
    
    while not do_quit:
        key = getch() #raw_input('Input:')
        #keyboard.read(1000, timeout = 0)
        if len(key):
            print key
            if key == 'q':
                do_quit = True
                break

# *** MAIN ***
if __name__ == "__main__":
    
    pygame.init()
    multiprocessing.log_to_stderr(logging.DEBUG)
    queue = multiprocessing.Queue()
    
#    q = multiprocessing.Queue()

    k = threading.Thread(target=keyLoop, args=())
    k.start()

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 80
        camera.vflip = True
        camera.hflip = True
        
        time.sleep(2)
        start = time.time()
        camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
        finish = time.time()
        print('Captured 40 images at %.2ffps' % (imgCnt / (finish - start)))

    k.join()
    print 'End?'
