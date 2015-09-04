import socket, traceback
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', 720))

print "Listening for broadcasts..."
print socket.gethostname()
host = socket.gethostname()

while 1:
    try:
        s.settimeout(2)
        message, address = s.recvfrom(8192)
        print "%s:\tGot message from %s: %s" % (time.ctime(), address, message)
        print socket.gethostbyaddr(address[0])
        client = socket.gethostbyaddr(address[0])[0]
        
        #time.sleep(1)
        s.sendto("Echo from "+ host +" : " + message, address)
        s.sendto("Hello from "+ client +" : ", address)
        print "Listening for broadcasts..."
    except  (socket.timeout):
        print '.'
    except (KeyboardInterrupt, SystemExit):
        print 'Exetption'
        raise
    except:
        print 'traceback'
        traceback.print_exc()
