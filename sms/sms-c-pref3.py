import socket
import sys
import time
from sms_pi import *
from sms_hub_lib4 import *
import multiprocessing

sm_wait = {} # Disse venter data
waiting = False


def xget_data():   
    print 'get_data in'
     
    while True:
        amount_received = 0
        print 'recv'
        msg = sock.recv(200)
        print 'get_data -> ' + msg
        if msg:
            
            l = msg.strip().split('\t')
            
            til = l[1].split('.')
            print til
            
            if til[-1] == 'Quit':
                print 'break'
                q.put(msg)
                break
                
        else:
            print 'get_data return'
            sock.close()
            return
            
        amount_received += len(msg)
        #print >>sys.stderr, 'received "%s"' % data
        q.put(msg)
    print 'get_data ut'
    
    
def xget_data2():   
    print 'get_data in2'
     
    while True:
        amount_received = 0
        print 'recv'
        msg = sock.recv(200)
        print 'get_data -> ' + str(msg)
        if msg:
            
            l = msg.strip().split('\t')
            
            til = l[1].split('.')
            print til
            
            if til[-1] == 'Quit':
                print 'break'
                q.put(msg)
                break
                
        else:
            print 'get_data return'
            sock.close()
            return
            
        amount_received += len(msg)
        #print >>sys.stderr, 'received "%s"' % data
        print 'w: ' + str(waiting) + '-' + l[1] + '\t' + l[0]
        if waiting == l[1] + '\t' + l[0]:
            q.put(msg)
        else:
            til = l[1].split('.')
            til.pop(0)
            l[2] = Disp_sm_pi(l[0], til, l[2], sock)
            if l[2]:
                data = l[1] + '\t' + l[0] + '\t' + l[2]
                print >>sys.stderr, 'sending data back: ' + data
                sock.sendall(data)
            
    print 'get_data ut2'
    
        
#def sm_wait_for(til):
    #q = multiprocessing.Queue() #    sm_wait[til] = q # Ma sjekke om den allerede eksisterer 
# msg = g.get()
#    del sm_wait[til]
    #return msg


def Xsm_func(fra, til, data):
    global waiting
    # Send data
    msg = fra + '\t' + til + '\t' + data + '\t#'
    print >>sys.stderr, 'Xsending "%s"' % msg
    
    PTD("Send")
    waiting = fra + '\t' + til
    sock.sendall(msg)
    #PTD("End")
    
    # Look for the response
    #get_data()

    msg = q.get()
    print 'wFalse'
    waiting = False
    
    if msg == '':
        return 'Abort'

    
    #PTD("Reseved")
    l = msg.strip().split('\t')
  
    return l[2]



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
    
finally:
    print "-> Quit: " + sock.sm_func(sysName, sysName + '.Quit', sysName) 
    print "UnRegName: " + sock.sm_func(sysName, 'Serv.UnRegName', sysName) 
#    q.put('')
         
    print >>sys.stderr, 'closing socket'
    sock.close()
