#import RPi.GPIO as GPIO
import time
import network

SWITCH = 10
s_on = True
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(SWITCH, GPIO.IN)

def heard(phrase):
  print "heard:" + phrase
  for a in phrase:
    if a == "\r" or a == "\n":
      pass # strip it
    else:
      if (True): #GPIO.input(SWITCH)):
        network.say("1")
      else:
        network.say("0")

while True:
  print "waiting for connection"
  network.wait(whenHearCall=heard)
  print "connected"

  while network.isConnected():
    print "server is running"  
    time.sleep(1)

  print "connection closed"
