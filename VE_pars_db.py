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


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

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

    
'''
db, cur = axs_cursor()

qry = 'select count(*) from axs_vepas'
print qry, ';'
cur.execute(qry)
for row in cur:
    print row
print '\n'

sLog.info('Close connection')
axs_close(db, cur)
'''

def AxTime(hex):
    if hex[0]=='#':
        return int(hex[1:], 16)/65536.0
    else:
        print "Mangler #!: ", hex
        return int(hex, 16)/65536.0
    

def sqlstr(s):
    return '"'+ str(s) + '"'


# time of last list
tol_3305 = -1
myTolList = {}

def getTol(axnr, lnr):
    try:
        res = myTolList[axnr][lnr]
            
    except:
        res = setTol(axnr, lnr, 0)
        
    return res
    
def setTol(axnr, lnr, val):
    try:
        myTolList[axnr][lnr] = val
            
    except:    
        myTolList[axnr] = [0,0,0,0, 0,0,0,0]
        myTolList[axnr][lnr] = val
        
    return val

# VePars  -  Parser og registrerer i db
class VePars:

    def __init__(self):
        self.i = 0

        # Get new cursor
        self.dbAxs, self.curAxs = axs_cursor()
        pass

    def closeDb(self):
        axs_close(self.dbAxs, self.curAxs)
        del self.dbAxs
        del self.curAxs

    @property
    def nextWord(self):
        self.i += 1
        s = self.ve[self.i - 1]
        return s


    def pars_vepas(self, vs, log):
        global tol_3305

        self.ve = vs.strip().split(',')

        dbAxs = self.dbAxs
        curAxs = self.curAxs

        #for i, e in enumerate(self.ve):
        #    print i ,': ', e

        assert self.ve[0] == 'VEPAS'

        axNr = self.ve[1]
        vNr = self.ve[2]
        lNr = self.ve[3]
        sType = self.ve[4]
        axT = AxTime(self.ve[5])
        tid = datetime.fromtimestamp(axT)

        tol = getTol(int(axNr), int(lNr))
        if tol == 0:
            td = 1000000
        else:
            td = (axT - tol)*1000.0

        setTol(int(axNr), int(lNr), axT)
        hast = 0

        sql =  'insert into axs_vepas ' \
           +' (`AXSPEED_ID`,`VEPAS_TYPE`,`V_NR`,`LINJE_ID`, `DATOTID`, `AxTid`, Tsl_ms) values ' \
           +' ( '+ axNr +', "'+ sType +'", '+ vNr +', '+ lNr +', '+ sqlstr(tid) +', '+ str(axT) +', '+ str(td) +' ) '

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

                hast = int(self.ve[i+2])
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

                hast = int(self.ve[i+0]) # kun forste aksel
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

            if (int(lNr) % 2) == 1:
                hast = -hast

            status = self.ve[i]
            sql = 'update axs_vepas ' \
                    +' set status = '+ status \
		            +' , Hast_mt_med = '+ str(hast) \
                    +' where axs_vepas_id = '+ str(vepas_id)
            log.debug( sql )
            curAxs.execute(sql)
            
            dbAxs.commit()
        except Exception as ex:                       
            dbAxs.rollback()
            log.info( 'Rollback:'+ vs)

            log.exception( str(ex) )
            raise


if __name__ == '__main__':
    # Test
    import unittest


    class Test_VE_pars(unittest.TestCase):

        def setUp(self):
            print 'In setUp()'
            self.vep = VePars()
            self.log = logging.getLogger('Test')
            logging.basicConfig(level=logging.INFO)

        def tearDown(self):
            print 'In tearDown()'
            self.vep.closeDb()
            del self.vep
            del self.log


        def test_RegName(self):
            print '\nRegName sm_serv'
            data = 'ACK'
            self.assertEqual(data, 'ACK')

        def test_Test_SP(self):
            self.vep.pars_vepas('VEPAS,3208,482444,2,SP,#56B3424A4A57,2,4235,0,663,123,129,4191,2722,666,124,129,96', self.log)

        def test_Test_SL(self):
            self.vep.pars_vepas('VEPAS,3305,809828,1,SL,#56B33C5C5EFD,1,3811,3914,4030,8208,7511,100', self.log)

        def test_Test_ST(self):
            self.vep.pars_vepas('VEPAS,3305,809831,0,ST,#56B33C7B3C80,1,3956,4015,3934,5300,5249,2,3951,0,603,2145,1128,3962,2564,599,2034,1010,100', self.log)

        def test_Test_SN(self):
            self.vep.pars_vepas('VEPAS,3199,925521,1,SN,56B340FFEFA9,0', self.log)


    # Run testcase
    unittest.main()