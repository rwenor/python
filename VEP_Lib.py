
#import pymssql
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


ve_0 = "VEPAS,3161,307621,2,SP,#568E906F1266,5,7426,0,2663,241,285,7429,3706,5349,423,580,7440,5711,3275,284,350,7444,1314,2897,256,312,7445,1316,2861,251,312,96"
ve_2 = "VEPAS,3306,1456,0,ST,#5698D63543FF,1,3636,3604,4341,9736,9910,2,3658,0,419,904,674,3644,2739,174,731,522,100"
ve_1 = "VEPAS,3306,1465,1,SL,#5698D6B3A732,1,4413,4497,4099,9666,9203,100"

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
vp.pars(ve_1)


dbAxs.close()