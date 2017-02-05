import multiprocessing
import socket
import sys
import time

from sms_hub_lib5 import *
from sms_pi import *

sm_wait = {} # Disse venter data
waiting = False



def pingSystem(name, n, m):
    t1 = time.time()
    res = -1
    sock.deb = False
    for i in xrange(0,n):
        t0 = time.time()
        for j in xrange(0,m):
            res = sock.sm_func(sysName, name + '.ping', '.')

        print(name, 'ping: ',i, (time.time() - t0)*1000 / m, 'ms', 'Result:', res)
        #time.sleep(0.1)

    print(i*j, "ping tok", time.time() - t1, 's')

    sock.deb = True


##### MAIN
if True: # len(sys.argv) < 3:

    sys.argv = ["Testing", "rwe1814.asuscomm.com", "Test1"]
    # sys.argv = ["Testing", "127.0.0.1", "Test1"]


sysName = sys.argv[2]

sock = SmsTcpClient( sys.argv[2], sys.argv[1], 9999)

## MAIN
try:
    print()
    print(1)

    print("-> RegName: " + sock.sm_func(sysName, 'Serv.RegName', sysName))
    print("-> Serv ping: " + sock.sm_func(sysName, 'Serv.ping', '.'))
    print("-> Serv.ListCli: " + sock.sm_func(sysName, 'Serv.ListCli', '.'))

    pingSystem('Serv', 4, 100)
    pingSystem('NodeClient', 4, 100)
    pingSystem('NodeClientPi', 4, 100)
    # pingSystem('GoPiGo', 4, 100)

    print(2, 'sleep 15 sec')
    time.sleep(15)
    print(3)

finally:
    print("-> Quit: " + sock.sm_func(sysName, sysName + '.Quit', sysName))
    print("UnRegName: " + sock.sm_func(sysName, 'Serv.UnRegName', sysName))
#    q.put('')

    print('closing socket')
    sock.close()
