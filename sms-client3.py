import socket
import sys
import time
from sms_pi import *


def con_recv(con, addr):
    try:
        print >>sys.stderr, 'connection from', addr
        
        while True:
            data = con.recv(200)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                l = data.strip().split('\t')
                if len(l) < 3:
                    print "Err: ", l
                    l[2] = 'NAK'
                else:
                    l[2] = Disp_sm(l[0], l[1], l[2], connection)

                #print >>sys.stderr, 'sending data back to the client'
                data = l[1] + '\t' + l[0] + '\t' + l[2]
                con.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', addr
                break
            
    finally:
        # Clean up the connection
        con.close()
        
    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (sys.argv[1], 9998)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

sysName = sys.argv[2]


def sm_func(fra, til, data):
    # Send data
    msg = fra + '\t' + til + '\t' + data
    print >>sys.stderr, 'sending "%s"' % msg
    
    #PTD("Send")
    sock.sendall(msg)
    #PTD("End")
    
    # Look for the response
    amount_received = 0
    
    while amount_received < 10:
        msg = sock.recv(200)
        amount_received += len(msg)
        #print >>sys.stderr, 'received "%s"' % data
    
    #PTD("Reseved")
    l = msg.strip().split('\t')
  
    return l[2]



try:
    
##    print 'Send ""'
##    sock.sendall('')
##    time.sleep(5)
    print "RegName: " + sm_func(sysName, 'Serv.RegName', sysName)
    print "Cpu temp: " + sm_func(sysName, 'Til.CpuTemp', '.')
    print "Add: " + sm_func(sysName, 'Til.Add', '24 56 78')
    
    # Send data
##    message = sysName + "\tTil.Add\t1 2 3 4 5 6 123.34"
##    print >>sys.stderr, 'sending "%s"' % message
##
##    PTD("Send")
##    sock.sendall(message)
##    PTD("End")

    t = time.time()
    while time.time() < t - 10:
        print "Cpu temp: " + sm_func(sysName, 'Til.CpuTemp', '.')
        time.sleep(2)
        
    print "UnRegName: " + sm_func(sysName, 'Serv.UnRegName', sysName)

    # Look for the response
    amount_received = 0
    amount_expected = 10
    
    while amount_received < 10:
        data = sock.recv(200)
        amount_received += len(data)
        print >>sys.stderr, 'Xreceived "%s"' % data
        if data:
            l = data.strip().split('\t')
            if len(l) < 3:
                print "Err: ", l
                l[2] = 'NAK'
            else:
                l[2] = Disp_sm_pi(l[0], l[1], l[2], sock)

            #print >>sys.stderr, 'sending data back to the client'
            data = l[1] + '\t' + l[0] + '\t' + l[2]
            sock.sendall(data)
        else:
            print >>sys.stderr, 'no more data from', addr
            break

    PTD("Reseved: " + str(amount_received))
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
