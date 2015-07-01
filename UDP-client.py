import socket, sys
dest = ('<broadcast>', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto("Hello from client", dest)
print "Listening for replies; press Ctrl-C to stop."
while 1:
    (buf, address) = s.recvfrom(2048)
    if not len(buf):
        print "Received NULL from %s: %s" % (address, buf)
        #break
    else:
        print "Received data from %s: %s" % (address, buf)
    #break
