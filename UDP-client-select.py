import socket, sys, select
import time

dest = ('<broadcast>', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
input = [s,sys.stdin] 

t0 = time.time()
s.sendto("Hello from client", dest)

print "Listening for replies; press Ctrl-C to stop."
cmd = ''

while cmd <> 'q':
    
  inputready,outputready,exceptready = select.select(input,[],[])

  #print inputready
  
  for src in inputready:

    t1 = time.time()  
    if src == s: 
        (buf, address) = s.recvfrom(2048)
        t1 = time.time()
        if not len(buf):
            print "%d -> Received NULL from %s: %s" % (t1 - t0, address, buf)
            #break

        else:
            print "%d -> Received data from %s: %s" % ((t1 - t0)*1000, address, buf)
            break
        
    elif src == sys.stdin:
        cmd = sys.stdin.readline().strip() 
        print "%d -> Received cmd: %s" % ((t1 - t0)*1000, cmd)

        if cmd == 'q':
            print 'Quit'
        elif cmd == 'r':
            t0 = time.time()
            s.sendto("Retransmit from client", dest)
        
    else:
        print "%d -> Data? from %s" % ((t1 - t0)*1000, str(src))

    print 'Cmd: ', cmd

