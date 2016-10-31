import socket
import select
import sys
import time
import os
import threading
from sms_pi import *
# import datetime

conDict = {}

servName = 'Serv'
DEBUG_ON = True

def printErr(msg):
    print('Err: ' + msg)

def deb(msg, always=0):  # Styres med DEBUG_ON, overide 1, never -1  
    if (DEBUG_ON and always > -1) or always > 0:
        print(msg)    

def nowstr():
    # now = datetime.datetime.now()
    return time.strftime("%Y-%m-%d %H:%H:%S"); 

def Disp_sm_SetName(name):
    servName = name

# 3: len(msg) 
# rest: msg
# msg = from to data (separated by tab)
def send_sm(con, msg):
    if (len(msg) <= 200):
        msg = str(len(msg)).zfill(3) + msg
        con.sendall(msg)
        # time.sleep(0.1)
    else:
        printErr('msg to long')


def recv_sm(con):
    try:
        l = int(con.recv(3))
        return con.recv(l)
    except Exception as e: 
        deb(e)
        pass

    # Exception ocurred
    return ''
    


def Disp_sm_serv(fra, til, data, con, serv):
    if til[0] == 'UnRegName':
        del conDict[data]
        data = 'BYE'
        # print conDict
    elif til[0] == 'RegName':
        conDict[data] = sms_client(data, '', con)
        data = 'ACK'
        # print conDict
    elif til[0] == 'GetName':
        data += str(len(conDict))
        conDict[data] = sms_client(data, '', con)
        # returner navn  data = 'ACK'
        # print conDict
    elif til[0] == 'ping':
        # conDict[data] = sms_client(data, '', con)
        data = 'ACK'
        # print conDict
    elif til[0] == 'ListCli':
        # print conDict
        # conDict[data] = sms_client(data, '', con)
        data = None
        for k, v in conDict.items():
            serv.sendSM(til, fra, k)
    else:
        # print 'DISP_SM'
        data = Disp_sm_pi(fra, til, data, con)

    return data


def Disp_sm_hub(fra, til, data, con, serv=None):
    # print '***DISP:'
    tlist = til.split('.')
    to = tlist.pop(0)

    # print 'YYYYYY'
    if to == servName:
        print('S',)
        data = Disp_sm_serv(fra, tlist, data, con, serv)

    elif to in conDict:
        print('^',)
        to_sm = conDict[to]
        msg = fra + '\t' + til + '\t' + data
        deb('<< "' + msg + '" --> ' + to_sm.cName)
        send_sm(to_sm.con, msg)
        # data = Disp_sm_pi(fra, til, data, con)
        data = None
    else:
        data = 'No srv: ' + to

    return data


class sms_client:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, con):
        self.cName = name
        self.cAddr = addr
        self.con = con


class SmsTcpServer:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, port):
        self.name = name
        self.addr = (addr, port)
        self.running = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        printErr('starting up on %s port %s' % self.addr)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.settimeout(10)
        self.sock.bind(self.addr)
        self.deb = DEBUG_ON

    def close(self):
        print('sock.closeing...')
        self.running = False
        # self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    @staticmethod
    def Xsendall(msg):
        print('xxxSending ""' + msg)

    def sendSM(self, fra, til, msg):
        # msg = self.name + '.' + '.'.join(fra) + '\t' + til + '\t' + msg
        if self.deb:
            print('<dx ', str(msg))
        Disp_sm_hub(self.name + '.' + '.'.join(fra), til, msg, None)

    def con_recv_hub(self, con, addr):
        try:
            printErr('connection from', addr)

            while True:
                # print 'Inn'
                data = recv_sm(con)  # con.recv(200)
                # print 'Ut'

                if data:
                    l = data.strip().split('\t')
                    if self.deb:
                        printErr('H>x "%s"' % str(len(l)) + ' : ' + data)

                    # Ekstra element?
                    if len(l) < 2:
                        print("Err: ", l)
                        if len(l) > 2:
                            l[2] = 'Err to long?'
                        else:
                            send_sm(con, "Err: " + data)
                            continue

                    else:
                        l[2] = Disp_sm_hub(l[0], l[1], l[2], con, self)

                    # print >>sys.stderr, 'sending data back to the client'
                    if l[2] is not None:
                        data = l[1] + '\t' + l[0] + '\t' + l[2]
                        send_sm(con, data)
                    if l[2] == 'BYE':
                        time.sleep(1)  # La svaret komme tilbake
                        break
                else:
                    break

            printErr('H: No more data from', addr)

        finally:
            # Clean up the connection
            print('Server closing connection')
            con.close()
            print(conDict)

    def run_server(self):
        # Listen for incoming connections
        self.sock.listen(1)
        self.running = True

        try:
            while self.running:
                # Wait for a connection
                # print conDict
                printErr('S: Waiting for a connection')

                connection, client_address = self.sock.accept()
                print('S: Accept: ', client_address)

                with open("sms-con.log", "a") as myf:
                    myf.write(str(client_address) + ' ' + nowstr() + "\n")

                # con_recv(connection, client_address)
                t = threading.Thread(target=self.con_recv_hub, args=(connection, client_address))
                t.start()

        finally:
            # print "Stop test1: " + sm_func(sysName, 'test1.Quit', sysName)
            # print "Stop test2: " + sm_func(sysName, 'test2.Quit', sysName)
            print("S: End.")


class SmsTcpClient:
    def __init__(self, name, addr, port, unik=True):
        self.name = name
        self.addr = (addr, port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        printErr('Connect to %s on port %s' % self.addr)
        self.sock.connect(self.addr)
        self.deb = DEBUG_ON
        self.waiting = None
        self.waitingMsg = ''

        # self.disp_sm = Disp_sm_pi
        self.t0 = time.time()
        if unik:
            self.sm_func(self.name, 'Serv.RegName', self.name)
        else:
            self.name = self.sm_func(self.name, 'Serv.GetName', self.name)

    def close(self):
        self.sm_func(self.name, 'Serv.UnRegName', self.name)
        self.sock.close()

    def send(self, msg):

        if self.deb:
            t1 = (time.time() - self.t0) * 1000
            print('<c ', "{:10.4f}".format(t1), str(msg))
            self.t0 = time.time()

        send_sm(self.sock, msg)

    def sendSM(self, fra, til, msg):
        msg = self.name + '.' + fra + '\t' + til + '\t' + msg
        if self.deb:
            # print '<c ', str(msg)
            t1 = (time.time() - self.t0) * 1000
            print('<s ', t1, str(msg))
            self.t0 = time.time()

        send_sm(self.sock, msg)

    def recv(self):
        msg = recv_sm(self.sock)
        if self.deb:
            t1 = (time.time() - self.t0) * 1000
            print('r> ', "{:10.4f}".format(t1), str(msg))
            self.t0 = time.time()
            # print 'c> ', str(msg)
        return msg

    def sm_rpc(self, til, data):
        # global waiting
        # global q

        # Send data
        fra = self.name + '.' + 'rpc'
        msg = fra + '\t' + til + '\t' + data + '\t#'
        # print >>sys.stderr, 'X-sending "%s"' % msg

        # PTD("Send")
        self.waitingMsg = fra + '\t' + til
        self.send(msg)
        # PTD("End")

        # Look for the response
        # get_data()

        # msg = q.get()
        # print 'wFalse'
        waiting = False

        msg = self.recv()
        if msg == '':
            return 'Abort'

        # PTD("Reseved")
        l = msg.strip().split('\t')

        return l[2]


    def sm_func(self, fra, til, data):
        # global waiting
        # global q

        # Send data
        msg = fra + '\t' + til + '\t' + data + '\t#'
        # print >>sys.stderr, 'X-sending "%s"' % msg

        # PTD("Send")
        self.waitingMsg = fra + '\t' + til
        self.send(msg)
        # PTD("End")

        # Look for the response
        # get_data()

        # msg = q.get()
        # print 'wFalse'
        waiting = False

        msg = self.recv()
        if msg == '':
            return 'Abort'

        # PTD("Reseved")
        l = msg.strip().split('\t')

        return l[2]


    def get_data2(self):
        print('XXX get_data in2')

        while True:
            amount_received = 0
            print('recv')
            msg = self.recv()
            print('get_data -> ' + str(msg))
            if msg:

                l = msg.strip().split('\t')

                til = l[1].split('.')
                print(til)

                if til[-1] == 'Quit':
                    print('break')
                    q.put(msg)
                    break

            else:
                print('get_data return')
                sock.close()
                return

            amount_received += len(msg)
            # print >>sys.stderr, 'received "%s"' % data
            # print 'w: ' + str(waiting) + '-' + l[1] + '\t' + l[0]
            if self.waiting == l[1] + '\t' + l[0]:
                q.put(msg)
            else:
                til = l[1].split('.')
                til.pop(0)
                l[2] = Disp_sm_pi(l[0], til, l[2], self.sock)
                if l[2]:
                    data = l[1] + '\t' + l[0] + '\t' + l[2]
                    printErr('sending data back: ' + data)
                    self.send(data)

        print('get_data ut2')

    def disp_sms(self, disp_func, timeout=0):

        inputready, outputready, exceptready = select.select([self.sock], [], [], timeout)

        # print inputready

        # Les fra socket
        for src in inputready:
            if src == self.sock:
                amount_received = 0
                # print 'recv'
                msg = self.recv()
                # print 'get_data -> ' + str(msg)
                if msg:

                    l = msg.strip().split('\t')

                    til = l[1].split('.')
                    # print til

                    if til[-1] == 'Quit':
                        print('break')
                        q.put(msg)

                else:
                    print('get_data return')
                    sock.close()
                    return

                amount_received += len(msg)
                # print >>sys.stderr, 'received "%s"' % data
                # print 'w: ' + str(self.waiting) + '-' + l[1] + '\t' + l[0]
                if self.waiting == l[1] + '\t' + l[0]:
                    q.put(msg)
                else:
                    print("--------------")
                    til = l[1].split('.')
                    til.pop(0)
                    l[2] = disp_func(l[0], til, l[2], self.sock)
                    if l[2]:
                        data = l[1] + '\t' + l[0] + '\t' + l[2]
                        printErr('sending data back: ' + data)
                        self.send(data)
                    return True

                    # print 'disp_sm ut2'


class test_con:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, con):
        self.cName = name
        self.cAddr = addr
        self.con = con

    def sendall(self, msg):
        print('Sending ""' + msg)


if __name__ == '__main__':
    # Test
    import unittest
    testPort = 9876


    class TestStringMethods (unittest.TestCase):

        def test_RegName(self):
            print('\nRegName sm_serv')
            data = Disp_sm_serv('Fra 1', 'RegName'.split('.'), 'Fra 1', test_con('Fra 1', '1.2.3.4', 1), None)
            self.assertEqual(data, 'ACK')
            print(conDict)

        def test_Disp(self):
            print('\nRegName sm_hub')
            data = Disp_sm_hub('Test.Fra 1', 'Serv.ping', 'Fra 1', None)
            self.assertEqual(data, 'ACK')
            print(conDict)

        def test_Disp_Send(self):
            print('\nDisp_Send')
            # Setup
            data = Disp_sm_hub('Test.Fra 1', 'Serv.RegName', 'Fra 1', test_con('Fra 1', '1.2.3.4', 1))
            self.assertEqual(data, 'ACK')
            print(conDict)

            # Send
            data = Disp_sm_hub('Test.Fra 1', 'Fra 1.Test', 'Data', '')
            self.assertEqual(data, None)
            print(conDict)

        def test_sm_Func(self):
            print('\nsm_Func')
            sm_wait = {'test': None}
            self.assertEqual(sm_wait['test'], None)
            del sm_wait['test']

            try:
                a = sm_wait['test']
            except KeyError:
                print('Key deleted')

                # self.assertEqual(sm_wait['test'], None)

        def xtest_server_client(self):
            serv = SmsTcpServer("Serv", '', testPort)
            t = threading.Thread(target=serv.run_server, args=())
            t.start()

            time.sleep(1)

            serv.running = False  # Stop server
            cli = SmsTcpClient("cli", '127.0.0.1', testPort)
            time.sleep(1)

            cli.send('test')
            msg = cli.recv()
            print('-> ' + msg)

            print("## RegName: " + cli.sm_func(cli.name, 'Serv.RegName', cli.name))
            print("## CpuTemp: " + cli.sm_func(cli.name, 'Serv.CpuTemp', '.'))
            print("## Quit: " + cli.sm_func(cli.name, cli.name + '.Quit', cli.name))

            self.assertEqual('BYE', cli.sm_func(cli.name, 'Serv.UnRegName', cli.name))

            # cleanup_stop_thread();

            # cli.sendall('') # Stop server thread
            cli.close()
            serv.close()
            # self.assertEqual('test1', msg)

        def xtest_server_client(self):
            serv = SmsTcpServer("Serv-test", '', testPort)
            t = threading.Thread(target=serv.run_server, args=())
            t.start()

            time.sleep(1)

            cli = SmsTcpClient("cli-test", '127.0.0.1', testPort)
            time.sleep(1)

            cli.sendSM('test', 'Serv.ListCli', '.')
            msg = cli.recv()
            print('-> ' + msg)

            print("## Quit: " + cli.sm_func(cli.name, cli.name + '.Quit', cli.name))

            serv.running = False  # Stop server after this
            self.assertEqual('BYE', cli.sm_func(cli.name, 'Serv.UnRegName', cli.name))

            # cleanup_stop_thread();

            # cli.sendall('') # Stop server thread
            cli.close()
            serv.close()
            # self.assertEqual('test1', msg)


    print(3 * '\n')
    print(70 * '*')
    print('Test: ')
    unittest.main()
