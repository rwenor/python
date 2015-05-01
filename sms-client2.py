import socket
import sys
import time



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
    print "Cpu temp: " + sm_func(sysName, 'Til.CpuTemp', '.')
    print "Add: " + sm_func(sysName, 'Til.Add', '24 56 78')
    
    # Send data
    message = sysName + "\tTil.Add\t1 2 3 4 5 6 123.34"
    print >>sys.stderr, 'sending "%s"' % message

    PTD("Send")
    sock.sendall(message)
    PTD("End")

    t = time.time()
    while time.time() < t + 10:
        print "Cpu temp: " + sm_func(sysName, 'Til.CpuTemp', '.')
        time.sleep(2)
        
    print "UnRegName: " + sm_func(sysName, 'Serv.UnRegName', sysName)

    # Look for the response
    amount_received = 0
    amount_expected = 10
    
    while amount_received < 10:
        data = sock.recv(200)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

    PTD("Reseved: " + str(amount_received))
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
