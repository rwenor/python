#!/usr/bin/env python
import logging
import os

import SocketServer
from threading import Thread

conCount = 0
totCon = 0
serverRun = True

class service(SocketServer.BaseRequestHandler):
    def handle_timeout(self):
        print 'Timeout ...'

    def handle(self):
        global conCount, totCon
        data = 'dummy'
        resCnt = 0

        self.request.settimeout(15)

        self.log = logging.getLogger(str(self.client_address))
        logging.basicConfig(level=logging.DEBUG)

        conCount += 1
        totCon += 1

        self.log.info('Connected from '+ str(self.client_address) +' #'+ str(conCount) + ':'+ str(totCon))
            
        ret = '200 Connected from '+ str(self.client_address) +' #'+ str(conCount) + ':'+ str(totCon)
        self.log.debug('< '+ ret)
        self.request.send(ret + '\r\n')
        
        # ta mot data til "." er motatt
        while len(data):
            
            try:
                data = ''
                while data[-1:] <> '\n':
                    data += self.request.recv(1024)
                    #for c in data[-2:]:
                    #    print c, ord(c)
                    
            except Exception as e:
                self.log.warning(str(e))
                break
    
            if not data:
                self.log.warning('Connection lost')
                break
            
            self.log.debug( str(resCnt) +'> '+ data.rstrip() +' -Len='+ str(len(data)))


            # Handle request
            if "." == data.rstrip():
                ret = '201 BYE'
            elif data[0] == 'V':
                ret = '210 OK'
                resCnt += 1
                # print resCnt,
            else:
                ret = '410 ERROR'


            if ret[:3] <> '210':
                self.log.debug('< '+ ret)

            self.request.send(ret + '\r\n')

            # END ???
            if "." == data.rstrip():  break
            if not serverRun:
                self.log.info('Server stopped')
                break

        # print "Client exited", self.client_address
        self.log.info("Client exit. VE_Cnt: "+ str(resCnt)) 
                      
        totCon -= 1
        self.request.close()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

SocketServer.ThreadingTCPServer.allow_reuse_address = True
# SocketServer.ThreadingTCPServer.timeout = 5
port = 9998 #os.getenv('PORT', '8080')
ip = '0.0.0.0' #os.getenv('IP', '0.0.0.0')
#print "Server on",  ip, port

t = ThreadedTCPServer((ip, port), service)

# t.setDaemon(True)
ip, port = t.server_address
print "Server on",  ip, port

try:
    t.serve_forever()
except:
    print "Stopping..."
    serverRun = False
    

