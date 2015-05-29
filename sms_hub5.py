import socket
import sys
import time
import os
import threading
from sms_pi import *
from sms_hub_lib2 import *

    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
#server_address = ('192.168.1.138', 999)
server_address = ('', 9999)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

try:
  while True:
    
    # Wait for a connection
    #print conDict
    print >>sys.stderr, 'waiting for a connection'

    connection, client_address = sock.accept()

    #con_recv(connection, client_address)
    t = threading.Thread(target = con_recv_hub, args = (connection, client_address))
    t.start()

finally:
    #print "Stop test1: " + sm_func(sysName, 'test1.Quit', sysName)
    #print "Stop test2: " + sm_func(sysName, 'test2.Quit', sysName)
    print "End."