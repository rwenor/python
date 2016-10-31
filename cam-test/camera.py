from picamera import PiCamera, Color
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.start_preview(alpha=100)

sleep(2)


camera.annotate_background = Color('blue')
camera.annotate_foreground = Color('yellow')
camera.annotate_text = " Hello world "
sleep(5)

camera.stop_preview()


