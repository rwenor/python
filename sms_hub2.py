import socket
import sys
import time
import os
import threading
from sms_pi import *


conDict = {}

def Disp_sm(fra, til, data, con):

    if til == 'Serv.UnRegName':
        del conDict[data]
        data = 'AKK'
    elif til == 'Serv.RegName':
        conDict[data] = sms_client(data, '', con)
        data = 'AKK'        
    else:
        data = Disp_sm_pi(fra, til, data, con)
            
    return data
    

class sms_client:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, con):
        self.cName = name
        self.cAddr = addr
        self.con = con
        


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

# Bind the socket to the port
#server_address = ('192.168.1.138', 999)
server_address = ('', 9998)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    
    # Wait for a connection
    print conDict
    print >>sys.stderr, 'waiting for a connection'

    connection, client_address = sock.accept()

    con_recv(connection, client_address)
    #t = threading.Thread(target = con_recv, args = (connection, client_address))
    #t.start()


