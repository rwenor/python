import socket
import sys
import time
from sms_pi import *
from sms_hub_lib4 import *
import multiprocessing

sm_wait = {} # Disse venter data
waiting = False




##### MAIN
if len(sys.argv) < 3:
    sys.argv = ["Testing", "127.0.0.1", "Test1"]


sysName = sys.argv[2]

sock = SmsTcpClient( sys.argv[2], sys.argv[1], 9999)

## MAIN
try:
#    q = multiprocessing.Queue()
    
#    k = threading.Thread(target=get_data2, args=())
#    k.start()
##    print 'Send ""'
##    sock.sendall('')
##    time.sleep(5)
    print
    print 1
    print "-> RegName: " + sock.sm_func(sysName, 'Serv.RegName', sysName)
    print "-> CpuTemp: " + sock.sm_func(sysName, 'Serv.CpuTemp', '.')
    print "-> CpuTemp: " + sock.sm_func(sysName, 'Serv.CpuTemp', '.')
    print "-> Test1.CpuTemp: " + sock.sm_func(sysName, 'Test1.CpuTemp', '.')

    for i in xrange(0,0):
        sock.sendall(sysName + '.Print\tServ.CpuTemp\t.')
        time.sleep(0.1)
        print i
        #print
        
    print 2    
    #time.sleep(15)
    print 3

    sock.get_data2()
    
finally:
    print "-> Quit: " + sock.sm_func(sysName, sysName + '.Quit', sysName) 
    print "UnRegName: " + sock.sm_func(sysName, 'Serv.UnRegName', sysName) 
#    q.put('')
         
    print >>sys.stderr, 'closing socket'
    sock.close()
