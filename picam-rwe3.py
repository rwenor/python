#!/usr/bin/python

# original script by brainflakes, improved by pageauc, peewee2 and Kesthal
# www.raspberrypi.org/phpBB3/viewtopic.php?f=43&t=45235

# You need to install PIL to run this script
# type "sudo apt-get install python-imaging-tk" in an terminal window to do this

import StringIO
import io
import subprocess
import os
import time
from datetime import datetime
from PIL import Image
import pygame
import picamera


# Motion detection settings:
# Threshold          - how much a pixel has to change by to be marked as "changed"
# Sensitivity        - how many changed pixels before capturing an image, needs to be higher if noisy view
# ForceCapture       - whether to force an image to be captured every forceCaptureTime seconds, values True or False
# filepath           - location of folder to save photos
# filenamePrefix     - string that prefixes the file name for easier identification of files.
# diskSpaceToReserve - Delete oldest images to avoid filling disk. How much byte to keep free on disk.
# cameraSettings     - "" = no extra settings; "-hf" = Set horizontal flip of image; "-vf" = Set vertical flip;
#                      "-hf -vf" = both horizontal and vertical flip
threshold = 40     # 10 diff
sensitivity = 40   # 20 cnt

forceCapture = True
forceCaptureTime = 60 * 60 # Once an hour

filepath = "/var/www/picam"
filenamePrefix = "cap"
diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
cameraSettings = "-hf -vf" # -awb shade -ISO 1600 -ss 100000"

# settings of the photos to save
saveWidth   = 640
saveHeight  = 480
saveQuality = 15 # Set jpeg quality (0 to 100)

# Test-Image settings
testWidth = 640
testHeight = 480

# this is the default setting, if the whole image should be scanned for changed pixel
testAreaCount = 1
#testBorders = [ [[1,testWidth],[testHeight,testHeight]] ]  # [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
testBorders = [ [[1,testWidth],[1,testHeight]] ]  # [ [[start pixel on left side,end pixel on right side],[start pixel on top side,stop pixel on bottom side]] ]
# testBorders are NOT zero-based, the first pixel is 1 and the last pixel is testWith or testHeight

# with "testBorders", you can define areas, where the script should scan for changed pixel
# for example, if your picture looks like this:
#
#     ....XXXX
#     ........
#     ........
#
# "." is a street or a house, "X" are trees which move arround like crazy when the wind is blowing
# because of the wind in the trees, there will be taken photos all the time. to prevent this, your setting might look like this:

#testAreaCount = 2
#testBorders = [ [[1,50],[1,75]], [[51,100],[26,75]] ] # area y=1 to 25 not scanned in x=51 to 100

# even more complex example
#testAreaCount = 4
#testBorders = [ [[1,39],[1,75]], [[40,67],[43,75]], [[68,85],[48,75]], [[86,100],[41,75]] ]

# in debug mode, a file debug.bmp is written to disk with marked changed pixel an with marked border of scan-area
# debug mode should only be turned on while testing the parameters above
debugMode = False       # False or True
#debugMode = True       # False or True
detectMotion = True    # If false object are detekted, continues pict


camera = picamera.PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.start_preview()
time.sleep(2)


# Capture a small test image (for motion detection)
def captureTestImage(settings, width, height):
    #command = "raspistill %s -w %s -h %s -t 200 -e jpg  -o -" % (settings, width, height)
    imageData = io.BytesIO()
    camera.capture(imageData, 'jpeg')
    # imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer

# Save a full size image to disk
def saveImage2(image2, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = filepath + "/" + filenamePrefix + "-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    #subprocess.call("raspistill %s -w %s -h %s -t 200 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), shell=True)
    image2.save(filename) # save debug image as bmp
    print "Captured %s" % filename

# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(filepath + "/")):
            if filename.startswith(filenamePrefix) and filename.endswith(".jpg"):
                os.remove(filepath + "/" + filename)
                print "Deleted %s/%s to avoid filling disk" % (filepath,filename)
                if (getFreeSpace() > bytesToReserve):
                    return

# Get available disk space
def getFreeSpace():
    st = os.statvfs(filepath + "/")
    du = st.f_bavail * st.f_frsize
    return du

# printTimeDiff
PrintTimeDiffLast = time.time()
PrintTimeCnt = 0

def PTD(str):
    global PrintTimeDiffLast
    global PrintTimeCnt
    print 'PTD%4s: %6s - %s' %  (PrintTimeCnt, \
                               int((time.time() - PrintTimeDiffLast)*1000), \
                               str) 
    PrintTimeCnt += 1
    PrintTimeDiffLast = time.time()


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
    print "Change: %s changed pixel, maxDiff = %s, 5 = %s 10 = %s, 15 = %s" % (changedPixels, maxDiff, cp5, cp10, cp15)
    
    if (debugMode):
        return changedPixels, takePicture, debugimage
    else:
        return changedPixels, takePicture, 0
    


# ************** START ****************
##pygame.mixer.init()
##s = pygame.mixer.Sound("/home/pi/python_games/match1.wav")
##pygame.mixer.music.set_volume(0.1)
##s.play()
##s.stop()

# Get first image
image1, buffer1 = captureTestImage(cameraSettings, testWidth, testHeight)
image0, buffer0 = captureTestImage(cameraSettings, testWidth, testHeight)

# Reset last capture time
lastCapture = time.time()
noMotionCnt = 0

while (True):

    # Get comparison image
    PTD('Start')
    image2, buffer2 = captureTestImage(cameraSettings, testWidth, testHeight)
    PTD('Cap')
    
    takePicture = False

    # Objekter?
    changedPixels0, takePicture0, debugimage = GetDiffDbImg(buffer0, buffer2)
    if (debugMode):
        debugimage.save(filepath + "/debug0.bmp") # save debug image as bmp
        #print "debug0.bmp saved, %s changed pixel" % (changedPixels0)

    # Bevegelse?
    changedPixels, takePicture, debugimage = GetDiffDbImg(buffer1, buffer2)
    if (debugMode):
        debugimage.save(filepath + "/debug.bmp") # save debug image as bmp
        #print "debug.bmp saved, %s changed pixel" % (changedPixels)

    if takePicture:
        takePicture = takePicture0 # Objekt i bilde?
    elif changedPixels < 10: # Ingen bevegelse
        noMotionCnt += 1
        if (noMotionCnt > 4) and (changedPixels < changedPixels0):
            image0 = image2  # Ny base
            buffer0 = buffer2        
    else:
        noMotionCnt = 0

    # Check force capture
    if forceCapture:
        if time.time() - lastCapture > forceCaptureTime:
            takePicture = True

    PTD('Pros')
    if takePicture:
        lastCapture = time.time()
        #image2.save(filepath + "/cam.jpg") # save debug image as bmp
        saveImage2(image2, diskSpaceToReserve)
        #saveImage(cameraSettings, saveWidth, saveHeight, saveQuality, diskSpaceToReserve)
#        s.play()

    # Swap comparison buffers
    if detectMotion:
        image1 = image2
        buffer1 = buffer2
        PTD('Swap')
