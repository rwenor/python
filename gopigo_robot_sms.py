#!/usr/bin/env python
#############################################################################################################                                                                  
# Basic example for controlling the GoPiGo using the Keyboard
# Controls:
#       w:      Move forward
#       a:      Turn left
#       d:      Turn right
#       s:      Move back
#       x:      Stop
#       t:      Increase speed
#       g:      Decrease speed
#       z:      Exit
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author        Date                    Comments  
# Karan                 27 June 14              Code cleanup                                                    
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
##############################################################################################################

from gopigo import *    #Has the basic functions for controlling the GoPiGo Robot
import sys      #Used for closing the running program

from sms.sms_pi import *
from sms.sms_hub_lib4 import SmsTcpClient



def Disp_sm_gopigo(fra, til, data, con):

    rdata = None
    #print fra, til, data
    if til[0] == 'cmd':

        a= til[1]   # Fetch the input from the terminal
        print a
        time.sleep(.1)
        
        if a=='w':
                fwd()   # Move forward
        elif a=='a':
                left()  # Turn left
        elif a=='o':
                
            for i in range(0,4):
                        fwd()
                        time.sleep(2)
                        stop()
                        time.sleep(0.1)
                        left()  # Turn left
                        time.sleep(0.5)
                        stop()
                        time.sleep(0.1) 
                        
            stop()
        elif a=='O':
                
            for i in range(0,4):
                        fwd()
                        time.sleep(0.1)
                        set_right_speed(128)
                        time.sleep(0.1)
                        set_left_speed(128)
                        time.sleep(2)
                        set_left_speed(64)  # Turn left
                        time.sleep(2)
            set_speed(0)
            
        elif a=='8':
                
                fwd()
                time.sleep(2)
                
                time.sleep(2)
                motor1(1, 50)
                motor2(1, 100)
                time.sleep(2)
                
                stop()
                
        elif a=='d':
                right() # Turn Right
        elif a=='s':
                bwd()   # Move back
                
        elif a=='ds':
                set_right_speed(int(data)) # Right speed
        elif a=='as':
                set_left_speed(int(data)) # Left speed
                
        elif a=='x':
            try:
                stop()  # Stop
            except:
                print 'Stop failed, try again...'
                time.sleep(0.2)
                stop()
                
        elif a=='t':
                increase_speed()        # Increase speed
        elif a=='g':
                decrease_speed()        # Decrease speed
        elif a=='v':
                print volt()
                rdata = str(volt())
        elif a=='z':
                print "Exiting"         # Exit
                stop()
                time.sleep(0.5)                
                sys.exit()
        else:
                print "Wrong Command, Please Enter Again"

        time.sleep(.1)
                
        
        
    elif til[0] == 'ping':

        rdata = 'ACK'

    else:
        #print 'DISP_SM'
        rdata = Disp_sm_pi(fra, til, data, con)
            
    return rdata




print "This is a basic example for the GoPiGo Robot control"
print "Press:\n\tw: Move GoPiGo Robot forward\n\ta: Turn GoPiGo Robot left\n\td: Turn GoPiGo Robot right\n\ts: Move GoPiGo Robot backward\n\tt: Increase speed\n\tg: Decrease speed\n\tx: Stop GoPiGo Robot\n\tz: Exit\n"


if len(sys.argv) < 3:
    sys.argv = ["GoPiGo_Test", "192.168.1.166", "GoPiGo"]
    
sms = SmsTcpClient( sys.argv[2], sys.argv[1], 9999)
print sms.sm_func(sms.name, 'Serv.RegName', sms.name)



# Set ned hastighet
for i in range(0, 0):
    time.sleep(1)
    decrease_speed()
    time.sleep(1)

print 'Redy to run'    

try: 
    while True:
        #time.sleep(0.1)
        sms.disp_sms( Disp_sm_gopigo, 3 )

finally:
    print 'Exit...'
    print sms.sm_func(sms.name, 'Serv.UnRegName', sms.name)
    print "BYE"
