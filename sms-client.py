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
server_address = ('10.0.0.130', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
##    print 'Send ""'
##    sock.sendall('')
##    time.sleep(5)
    
    # Send data
    message = "Fra\tTil.Add\t1 2 3 4 5 6 123.34"
    print >>sys.stderr, 'sending "%s"' % message

    PTD("Send")
    sock.sendall(message)
    PTD("End")

    # Look for the response
    amount_received = 0
    amount_expected = 10
    
    while amount_received < 10:
        data = sock.recv(200)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

    PTD("Reseved")
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
