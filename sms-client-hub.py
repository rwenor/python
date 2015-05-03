import socket
import sys
import time
from sms_pi import *
from sms_hub_lib import *
    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (sys.argv[1], 9999)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

sysName = sys.argv[2]


def sm_func(fra, til, data):
    # Send data
    msg = fra + '\t' + til + '\t' + data
    print >>sys.stderr, 'sending "%s"' % msg
    
    PTD("Send")
    sock.sendall(msg)
    PTD("End")
    
    # Look for the response
    amount_received = 0
    
    while amount_received < 10:
        msg = sock.recv(200)
        amount_received += len(msg)
        #print >>sys.stderr, 'received "%s"' % data
    
    PTD("Reseved")
    l = msg.strip().split('\t')
  
    return l[2]



try:
    
##    print 'Send ""'
##    sock.sendall('')
##    time.sleep(5)
    print "RegName: " + sm_func(sysName, 'Serv.RegName', sysName)
    print "Cpu temp: " + sm_func(sysName, 'Serv.CpuTemp', '.')
    print "Add: " + sm_func(sysName, 'Serv.Add', '24 56 78')
    

    t = time.time()
    tempsum = ''
    
    while time.time() < t + 10:
        temp = sm_func(sysName, 'Serv.CpuTemp', '.')
        tempsum += ' ' + temp 
        print "Cpu temp: " + temp
        print "Sum temp: " + sm_func(sysName, 'test2' + '.Add', tempsum)
        time.sleep(2)
        
    #print "UnRegName: " + sm_func(sysName, 'Serv.UnRegName', sysName)
    if sysName == 'test1':
         print "Stop test2: " + sm_func(sysName, 'test2.Quit', sysName)
         exit

    # Look for the response
    amount_received = 0
    amount_expected = 10
    
    while amount_received < 200:
        data = sock.recv(200)
        amount_received = len(data)
        print >>sys.stderr, 'Xreceived "%s"' % data
 
        if data:
          l = data.strip().split('\t')
          if len(l) < 3:
            print "Err: ", l
            l[2] = 'NAK'
          else:
            til = l[1].split('.')
            to = til.pop(0)
            
            print '# ' + data
            if til <> ['Quit']:
                if til:
                    l[2] = Disp_sm_pi(l[0], til, l[2], sock)
                else:
                    print '* ' + data
            else:
                print >>sys.stderr, 'no more data from', l[0]
                data = l[1] + '\t' + l[0] + '\t' + l[1] + ' Bye'
                sock.sendall(data)
                break              
                
            if l[2] <> None:
                data = l[1] + '\t' + l[0] + '\t' + l[2]
                sock.sendall(data)
                
        else:
            print 'No more? *'
            break 

    PTD("Reseved: " + str(amount_received) + ' - ' + data)
    
finally:
    print "UnRegName: " + sm_func(sysName, 'Serv.UnRegName', sysName) 
         
    print >>sys.stderr, 'closing socket'
    sock.close()
