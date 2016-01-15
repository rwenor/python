#!/usr/bin/env python
import logging
import os

import SocketServer
from threading import Thread

conCount = 0
totCon = 0
serverRun = True

from ConfigParser import SafeConfigParser
import MySQLdb
import time

from datetime import datetime

cfg = SafeConfigParser()
cfg.read('axs_serv.ini')
host = cfg.get('axs_db', 'host')
user = cfg.get('axs_db', 'user')
passwd = cfg.get('axs_db', 'passwd')
db = cfg.get('axs_db', 'db')

dbAxs = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
curAxs = dbAxs.cursor()

qry = 'select count(*) from axs_vepas'
print qry, ';'
curAxs.execute(qry)
for row in curAxs:
    print row
print '\n'


def AxTime(hex):
    assert(hex[0]=='#')
    return int(hex[1:], 16)/65535.0


def sqlstr(s):
    return '"'+ str(s) + '"'


class VePars:

    def __init__(self):
        self.i = 0
        pass

    @property
    def nextWord(self):
        self.i += 1
        s = self.ve[self.i - 1]
        return s


    def pars(self, vs):
        #global

        self.ve = vs.strip().split(',')

        for e in self.ve:
            print e

        assert self.ve[0] == 'VEPAS'

        axNr = self.ve[1]
        vNr = self.ve[2]
        lNr = self.ve[3]
        sType = self.ve[4]
        axT = AxTime(self.ve[5])
        tid = datetime.fromtimestamp(axT)

        sql =  'insert into axs_vepas ' \
           +' (`AXSPEED_ID`,`VEPAS_TYPE`,`V_NR`,`LINJE_ID`, `DATOTID`, `AxTid`) values ' \
           +' ( '+ axNr +', "'+ sType +'", '+ vNr +', '+ lNr +', '+ sqlstr(tid) +', '+ str(axT) +' ) '

        print sql
        try:
            curAxs.execute(sql)
            vepas_id = curAxs.lastrowid

            if sType in ['SL', 'ST']:
                i = 6

                i = 6 + 6
            else:
                i = 6

            # Pieco
            if sType in ['SP', 'ST']:

                axCnt = self.ve[i+0]  # Axsler ant


                sql = 'update axs_vepas ' \
                    +' set ANT_A = '+ axCnt \
                    +' where axs_vepas_id = '+ str(vepas_id)

                print sql
                curAxs.execute(sql)

                for j in range(1, int(axCnt) + 1):
                    sql = 'insert into axs_vepas_p ' \
                        +' (AXS_VEPAS_ID, AXS_VEPAS_AKSEL_NR ' \
                        +' , A_HAST, A_AVST, A_VEKT, A_S1, A_S2 ) '\
                        +' values ' \
                        +' ( '+ str(vepas_id) +', '+ str(j) \
                        +' , '+ self.ve[i+1]  \
                        +' , '+ self.ve[i+2]  \
                        +' , '+ self.ve[i+3]  \
                        +' , '+ self.ve[i+4]  \
                        +' , '+ self.ve[i+5]  \
                        +' )'
                    i += 5

                    print sql
                    curAxs.execute(sql)

            dbAxs.commit()
        except:
            dbAxs.rollback()
            print 'Rollback'
            raise

vp = VePars()


class service(SocketServer.BaseRequestHandler):
    def handle_timeout(self):
        print 'Timeout ...'

    def handle(self):
        global conCount, totCon
        global vp
        
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


                # Try
                vp.pars(data)
                
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
    
dbAxs.close()
