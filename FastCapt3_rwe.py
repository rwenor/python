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


debugMode = True       # False or True
testAreaCount = 1
testBorders = [ [[1,testWidth],[1,testHeight]] ]  # [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
threshold = 40     # 10 diff
sensitivity = 40   # 20 cnt

# Beregnerer diff og gir debug bilde
def GetDiffDbImg(buffer1, buffer2):
    #PTD('GetDiffDbImg')
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
    
    #PTD('End')
    dprt( "Change: %s changed pixel, maxDiff = %s, 5 = %s 10 = %s, 15 = %s" % (changedPixels, maxDiff, cp5, cp10, cp15))
    
    if (debugMode):
        return changedPixels, takePicture, debugimage
    else:
        return changedPixels, takePicture, 0
    
buf0 = None
buf1 = None

def img_load(stream,i):
    global buf0
    global buf1
    
    img = Image.open(stream)
    buffer = img.load()
    if i == 0:
        buf0 = buffer
        buf1 = buffer
            
    dprt('Loaded')
    changedPixels0, takePicture0, debugimage = GetDiffDbImg(buf1, buffer)
    dprt('Moved')
    


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
        time.sleep(0.2) # let tread start...
        
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
    
