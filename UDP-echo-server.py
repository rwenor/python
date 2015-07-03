import socket, traceback
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', 5000))

print "Listening for broadcasts..."

while 1:
    try:
        message, address = s.recvfrom(8192)
        print "%s:\tGot message from %s: %s" % (time.ctime(), address, message)
        
        time.sleep(1)
        s.sendto("Hello from server", address)
        print "Listening for broadcasts..."
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
