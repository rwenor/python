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


def recvLine(sock):
    data = ''
    while data[-1:] <> '\n':
        data += sock.recv(1024)
        #print >>sys.stderr, 'received "%s"' % data
        
    return data
    
    
    
PTD("Start")    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('rwe1814.asuscomm.com', 9998)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    data = recvLine(sock)
    print '>', data,

    PTD("1000 linjer")
    for i in range(1, 2):
        # sock.sendall('VE test: ...DDD.s.ds.ds.ds.dsds::::::::...'+ str(i) +'\r\n')
        sock.sendall('VEPAS,3306,1460,0,ST,#5698D64BA887,1,3816,3794,4143,7335,7377,2,3845,0,393,977,715,3829,2633,194,916,651,100\r\n')
        data = recvLine(sock)
        print i,
        if i % 10 == 0:
            print '*'

    sock.sendall('.\r\n')
    data = recvLine(sock)
    print '>', data,

    PTD("Done")
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
