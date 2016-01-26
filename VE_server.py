#!/usr/bin/env python
import logging
import os
import sys

import SocketServer
from threading import Thread

conCount = 0
totCon = 0
serverRun = True

from ConfigParser import SafeConfigParser
import MySQLdb
import time

from datetime import datetime


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sLog = logging.getLogger('Server')
fLog = sLog 




def axs_getdb():
    cfg = SafeConfigParser()
    cfg.read('axs_serv.ini')
    return MySQLdb.connect(host=cfg.get('axs_db', 'host'),
                                    user=cfg.get('axs_db', 'user'),
                                    passwd=cfg.get('axs_db', 'passwd'),
                                    db=cfg.get('axs_db', 'db'))

def axs_cursor():   
    #if not dbAxs.open:
    #    sLog.debug('Connect...')

    dbAxs = axs_getdb()

    sLog.debug('New db cursor')
    return dbAxs, dbAxs.cursor()


def axs_close(dbAxs, curAxs):
    sLog.debug('Close db')
    curAxs.close()
    dbAxs.close()


    
db, cur = axs_cursor()

qry = 'select count(*) from axs_vepas'
print qry, ';'
cur.execute(qry)
for row in cur:
    print row
print '\n'

sLog.info('Close connection')
axs_close(db, cur)

db, cur = axs_cursor()
qry = 'select count(*) from axs_vepas'
print qry, ';'
cur.execute(qry)
for row in cur:
    print row
print '\n'

sLog.info('Close connection')
axs_close(db, cur)


def AxTime(hex):
    if hex[0]=='#':
        return int(hex[1:], 16)/65536.0
    else:
        print "Mangler #!: ", hex
        return int(hex, 16)/65536.0
    

def sqlstr(s):
    return '"'+ str(s) + '"'


def addToVE(s):
    with open("VE_ok.dat", "a") as myfile:
        myfile.write(s)


def addToFail(s):
    with open("failVE.dat", "a") as myfile:
        myfile.write(s)

        
class VePars:

    def __init__(self):
        self.i = 0
        pass

    @property
    def nextWord(self):
        self.i += 1
        s = self.ve[self.i - 1]
        return s


    def pars(self, vs, dbAxs, curAxs, log):

        self.ve = vs.strip().split(',')

        #for i, e in enumerate(self.ve):
        #    print i ,': ', e

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

        log.debug( sql )
        try:
            curAxs.execute(sql)
            vepas_id = curAxs.lastrowid

            if sType in ['SL', 'ST']:
                i = 6
                sql = 'insert into axs_vepas_l ' \
                   +' (AXS_VEPAS_ID, ANT_V, LF_H,LE_H, L_L, LF_S, LE_S ) ' \
                   +' values ' \
                   +' ( '+ str(vepas_id) \
                   +' , '+  self.ve[i+0]  \
                   +' , '+  self.ve[i+1]  \
                   +' , '+  self.ve[i+2]  \
                   +' , '+  self.ve[i+3]  \
                   +' , '+  self.ve[i+4]  \
                   +' , '+  self.ve[i+5]  \
                   +' ) '
                i = 6 + 6

                log.debug( sql )
                curAxs.execute(sql)

            else:
                i = 6

            # Pieco
            if sType in ['SP', 'ST']:

                axCnt = self.ve[i+0]  # Axsler ant
                i += 1
                sql = 'update axs_vepas ' \
                    +' set ANT_A = '+ axCnt \
                    +' where axs_vepas_id = '+ str(vepas_id)

                log.debug( sql )
                curAxs.execute(sql)

                for j in range(1, int(axCnt) + 1):
                    sql = 'insert into axs_vepas_p ' \
                        +' (AXS_VEPAS_ID, AXS_VEPAS_AKSEL_NR ' \
                        +' , A_HAST, A_AVST, A_VEKT, A_S1, A_S2 ) '\
                        +' values ' \
                        +' ( '+ str(vepas_id) +', '+ str(j) \
                        +' , '+ self.ve[i+0]  \
                        +' , '+ self.ve[i+1]  \
                        +' , '+ self.ve[i+2]  \
                        +' , '+ self.ve[i+3]  \
                        +' , '+ self.ve[i+4]  \
                        +' )'
                    i += 5

                    log.debug( sql )
                    curAxs.execute(sql)


            
            # log.debug( 'status: '+ str(i) ) # status );

            status = self.ve[i]
            sql = 'update axs_vepas ' \
                    +' set status = '+ status \
                    +' where axs_vepas_id = '+ str(vepas_id)
            log.debug( sql )
            curAxs.execute(sql)
            
            dbAxs.commit()
        except Exception as ex:                       
            dbAxs.rollback()
            log.info( 'Rollback:'+ vs)

            log.exception( str(ex) )
            raise

vp = VePars()


class service(SocketServer.BaseRequestHandler):
    def handle_timeout(self):
        print 'Timeout ...'

    def handle(self):
        global conCount, totCon
        global vp

        self.log = logging.getLogger(str(self.client_address))
        logging.basicConfig(level=logging.DEBUG)
        log = self.log
        
        data = 'dummy'
        resCnt = 0

        self.request.settimeout(15)

        conCount += 1
        totCon += 1

        log.info('Connected from '+ str(self.client_address) +' #'+ str(conCount) + ':'+ str(totCon))
        log.info('Tid: '+ str(datetime.now()) )
            
        ret = '200 Connected from '+ str(self.client_address) +' #'+ str(conCount) + ':'+ str(totCon)
        log.debug('< '+ ret)
        self.request.send(ret + '\r\n')

        # Get new cursor
        dbAxs, curAxs = axs_cursor()
        
        # ta mot data til "." er motatt
        while len(data):
            
            try:
                data = ''
                while data[-1:] <> '\n':
                    data += self.request.recv(1024)
                    #for c in data[-2:]:
                    #    print c, ord(c)
                    
            except Exception as e:
                log.exception(str(e))
                break
    
            if not data:
                self.log.warning('Connection lost')
                break
            
            log.debug( str(resCnt) +'> '+ data.rstrip() +' -Len='+ str(len(data)))


            # Handle request
            if "." == data.rstrip():
                ret = '201 BYE'
            elif data[0] == 'V':

                try:
                    vp.pars(data, dbAxs, curAxs, log)
                    addToVE(data)
                    ret = '210 OK'
                    resCnt += 1
                    #print "210 OK: ", resCnt,
                except Exception as ex:
                    addToFail(data)
                    log.error('*** Parse feil: '+ str( ex ))
                    ret = '410 ERROR'
                
                
            else:
                addToFail(data)
                ret = '410 ERROR'


            if ret[:3] <> '210':
                log.debug('< '+ ret)

            self.request.send(ret + '\r\n')

            # END ???
            if "." == data.rstrip():  break
            if not serverRun:
                log.info('Server stopped')
                break

        # print "Client exited", self.client_address
        
        axs_close(dbAxs, curAxs)
        log.info("Client exit. VE_Cnt: "+ str(resCnt)) 
                      
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
