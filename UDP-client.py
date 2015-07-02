import socket, sys
import time

dest = ('<broadcast>', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto("Hello from client", dest)
t0 = time.time()

print "Listening for replies; press Ctrl-C to stop."
while 1:
    (buf, address) = s.recvfrom(2048)
    t1 = time.time()
    if not len(buf):
        print "%d -> Received NULL from %s: %s" % (t1 - t0, address, buf)
        #break
    else:
        print "%d -> Received data from %s: %s" % ((t1 - t0)*1000, address, buf)
    #break
