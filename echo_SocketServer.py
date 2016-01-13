#!/usr/bin/env python
import logging

import SocketServer
from threading import Thread

class service(SocketServer.BaseRequestHandler):
    def handle(self):
        data = 'dummy'
        print "Client connected with ", self.client_address
        # self.log = logging.getLogger(str(self.client_address))
        
        # ta mot data til "." er motatt
        while len(data):
            data = self.request.recv(1024)
            
            #self.log.info(data)
            print  self.client_address,  data.rstrip() 
            self.request.send(data)
            
            if "." == data.rstrip():  break

        print "Client exited", self.client_address
        self.request.close()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

t = ThreadedTCPServer(('0.0.0.0',9997), service)
# t.setDaemon(True)
ip, port = t.server_address
print "Server on",  ip, port
t.serve_forever()

