#!/usr/bin/env python
import logging

import SocketServer
from threading import Thread

conCount = 0
totCon = 0

class service(SocketServer.BaseRequestHandler):
    def handle_timeout(self):
        print 'Timeout ...'

    def handle(self):
        global conCount, totCon
        data = 'dummy'

        self.request.settimeout(15)

        self.log = logging.getLogger(str(self.client_address))
        logging.basicConfig(level=logging.DEBUG)

        conCount += 1
        totCon += 1

        ret = '200 Connected from '+ str(self.client_address) +' #'+ str(conCount) + ':'+ str(totCon)
        self.log.debug('< '+ ret)
        self.request.send(ret + '\n')
        
        # ta mot data til "." er motatt
        while len(data):
            data = self.request.recv(1024)
            self.log.debug('> '+ data.rstrip())


            # Handle request
            if "." == data.rstrip():
                ret = '201 BYE'
            elif data[0] == 'V':
                ret = '210 OK'
            else:
                ret = '404 ERROR'

            self.log.debug('< '+ ret)
            self.request.send(ret + '\n')

            # END ???
            if "." == data.rstrip():  break

        print "Client exited", self.client_address
        totCon -= 1
        self.request.close()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

SocketServer.ThreadingTCPServer.allow_reuse_address = True
# SocketServer.ThreadingTCPServer.timeout = 5

t = ThreadedTCPServer(('0.0.0.0',9999), service)

# t.setDaemon(True)
ip, port = t.server_address
print "Server on",  ip, port
t.serve_forever()

