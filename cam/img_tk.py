#!/usr/bin/env python

"""This is a small script to demonstrate using Tk to show PIL Image objects.
The advantage of this over using Image.show() is that it will reuse the
same window, so you can show multiple images without opening a new
window for each image.

This will simply go through each file in the current directory and
try to display it. If the file is not an image then it will be skipped.
Click on the image display window to go to the next image.

Noah Spurrier 2007
"""

import os, sys
import io
import Tkinter
import Image, ImageTk
import time
import picamera

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.

root = Tkinter.Tk()
root.bind("<Button>", button_click_exit_mainloop)
root.geometry('+%d+%d' % (100,100))
dirlist = os.listdir('.')
old_label_image = None

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)
    
    start = time.time()
    stream = io.BytesIO()
    i = 0
    print "Start"
    #for foo in camera.capture_continuous(stream, 'jpg'):
    while True:
        camera.capture('foo.jpg')
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent

        print "stream.tell()"
        
        # Rewind the stream and send the image data over the wire
        #stream.seek(0)
        print 'Done:', i

        image1 = Image.open('foo.jpg')
        root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(root, image=tkpi)
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])

        if False:
            print 'mainloop'
            root.mainloop() # wait until user clicks the window
        else:
            print 'update'
            root.update_idletasks()
            root.update()
        
        # If we've been capturing for more than 30 seconds, quit
        if time.time() - start > 30:
            break

        
        stream.truncate()

        i += 1


