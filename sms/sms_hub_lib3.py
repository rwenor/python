import socket
import sys
import time
import os
import threading
from sms_pi import *


conDict = {}

servName = 'Serv'

def Disp_sm_SetName(name):
    servName = name
    
    
def Disp_sm_serv(fra, til, data, con):

    if til[0] == 'UnRegName':
        del conDict[data]
        data = 'BYE'
        print conDict
    elif til[0] == 'RegName':
        conDict[data] = sms_client(data, '', con)
        data = 'ACK'
        print conDict
    elif til[0] == 'ping':
        conDict[data] = sms_client(data, '', con)
        data = 'ACK'
        print conDict
    else:
        print 'DISP_SM'
        data = Disp_sm_pi(fra, til, data, con)
            
    return data
    
    
def Disp_sm_hub(fra, til, data, con):

    print '***DISP:'
    tlist = til.split('.')
    to = tlist.pop(0)
    
    #print 'YYYYYY'
    if to == servName:
        print '***SERVER:'
        data = Disp_sm_serv(fra, tlist, data, con)
        
    elif to in conDict:
        print '***HUB:'
        to_sm = conDict[to]
        msg = fra + '\t' + til + '\t' + data
        print '<< "' + msg + '" --> ' + to_sm.cName
        to_sm.con.sendall(msg)
        #data = Disp_sm_pi(fra, til, data, con)
        data = None
    else:
        data = 'No srv: '+ to
            
    return data


def con_recv_hub(con, addr):
    try:
        print >>sys.stderr, 'connection from', addr
        
        while True:
            print 'Inn'
            data = con.recv(200)
            print 'Ut'
            
            if data:
                l = data.strip().split('\t')
                print >>sys.stderr, '>> "%s"' % str(len(l)) + ' : ' + data

                ## Ekstra element?
                if len(l) < 2:
                    print "Err: ", l
                    if len(l) > 2:
                        l[2] = 'Err to long?'
                    else:
                        continue
                    
                else:
                    l[2] = Disp_sm_hub(l[0], l[1], l[2], con)

                #print >>sys.stderr, 'sending data back to the client'
                if l[2] <> None:
                    data = l[1] + '\t' + l[0] + '\t' + l[2]
                    con.sendall(data)
                if l[2] == 'BYE':
                    time.sleep(1) # La svaret komme tilbake
                    break
            else:
                break
            
        print >>sys.stderr, 'no more data from', addr
            
    finally:      
        # Clean up the connection
        print 'Server closing connection'
        con.close()
    



class sms_client:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, con):
        self.cName = name
        self.cAddr = addr
        self.con = con
        
class test_con:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, con):
        self.cName = name
        self.cAddr = addr
        self.con = con
        
    def sendall(self, msg):
        print 'Sending ""' + msg 

class SmsTcpServer:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, port):
        self.name = name
        self.addr = (addr, port)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print >>sys.stderr, 'starting up on %s port %s' % self.addr
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        
        
    def close(self):
        print 'sock.closeing...'
        self.running = False
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close();


    def sendall(self, msg):
        print 'xxxSending ""' + msg


    def run_server(self):
        # Listen for incoming connections
        self.sock.listen(1)
        self.running = True

        try:
          while self.running:
            
            # Wait for a connection
            #print conDict
            print >>sys.stderr, 'waiting for a connection'

            connection, client_address = self.sock.accept()
            print 'Serv: accept'

            #con_recv(connection, client_address)
            t = threading.Thread(target = con_recv_hub, args = (connection, client_address))
            t.start()

        finally:
            #print "Stop test1: " + sm_func(sysName, 'test1.Quit', sysName)
            #print "Stop test2: " + sm_func(sysName, 'test2.Quit', sysName)
            print "End."
        
        
class SmsTcpClient:
    cName = ''
    cAddr = ''
    con = None

    def __init__(self, name, addr, port):
        self.name = name
        self.addr = (addr, port)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print >>sys.stderr, 'Connect to %s on port %s' % self.addr
        self.sock.connect(self.addr)
        self.deb = True


    def close(self):
        self.sock.close();

        
    def sendall(self, msg):
        if self.deb:
            print '<< ' + str(msg)
        if (len(msg) <= 200):
            #msg = str(len(msg)).zfill(3) + msg
            self.sock.sendall(msg)
            #time.sleep(0.1)
        else:
            print >>sys.stderr, 'msg to long'
            

    def recv(self, cnt):
        msg = self.sock.recv(cnt)
        if self.deb:
            print '>> ', str(msg)
        return msg
        
        
    def sm_func(self, fra, til, data):
        #global waiting
        #global q
        
        # Send data
        msg = fra + '\t' + til + '\t' + data + '\t#'
        #print >>sys.stderr, 'X-sending "%s"' % msg
    
        #PTD("Send")
        self.waitingMsg = fra + '\t' + til
        self.sendall(msg)
        #PTD("End")
    
        # Look for the response
        #get_data()

        #msg = q.get()
        #print 'wFalse'
        #waiting = False
    
        msg = self.recv(200)
        if msg == '':
            return 'Abort'

    
        #PTD("Reseved")
        l = msg.strip().split('\t')
  
        return l[2]


    def get_data2(self):   
        print 'get_data in2'
     
        while True:
            amount_received = 0
            print 'recv'
            msg = self.sock.recv(200)
            print 'get_data -> ' + str(msg)
            if msg:
            
                l = msg.strip().split('\t')
            
                til = l[1].split('.')
                print til
            
                if til[-1] == 'Quit':
                    print 'break'
                    q.put(msg)
                    break
                
            else:
                print 'get_data return'
                sock.close()
                return
            
            amount_received += len(msg)
            #print >>sys.stderr, 'received "%s"' % data
            print 'w: ' + str(waiting) + '-' + l[1] + '\t' + l[0]
            if waiting == l[1] + '\t' + l[0]:
                q.put(msg)
            else:
                til = l[1].split('.')
                til.pop(0)
                l[2] = Disp_sm_pi(l[0], til, l[2], sock)
                if l[2]:
                    data = l[1] + '\t' + l[0] + '\t' + l[2]
                    print >>sys.stderr, 'sending data back: ' + data
                    sock.sendall(data)
            
        print 'get_data ut2'


        
if __name__ == '__main__':
    ## Test    
    import unittest

    class TestStringMethods(unittest.TestCase):

      def xtest_RegName(self):
          print '\nRegName sm_serv'
          data = Disp_sm_serv('Fra 1', 'RegName'.split('.'), 'Fra 1', test_con('Fra 1', '1.2.3.4', 1))
          self.assertEqual(data, 'ACK')
          print conDict

      def xtest_Disp(self):
          print '\nRegName sm_hub'
          data = Disp_sm_hub('Test.Fra 1', 'Serv.RegName', 'Fra 1', test_con('Fra 1', '1.2.3.4', 1))
          self.assertEqual(data, 'ACK')
          print conDict

      def xtest_Disp_Send(self):
          print '\nDisp_Send'
          # Setup
          data = Disp_sm_hub('Test.Fra 1', 'Serv.RegName', 'Fra 1', test_con('Fra 1', '1.2.3.4', 1))
          self.assertEqual(data, 'ACK')
          print conDict
      
          # Send
          data = Disp_sm_hub('Test.Fra 1', 'Fra 1.Test', 'Data', '')
          self.assertEqual(data, None)
          print conDict
            
      def xtest_sm_Func(self):
          print '\nsm_Func'
          sm_wait = {}
          sm_wait['test'] = None
          self.assertEqual(sm_wait['test'], None)
          del sm_wait['test']
          
          try:
              a = sm_wait['test']
          except KeyError:
              print 'Key deleted'
              
          #self.assertEqual(sm_wait['test'], None)
          
      def test_server_client(self):
          serv = SmsTcpServer("Serv", '', 9999)
          t = threading.Thread(target = serv.run_server, args = ())
          t.start()
          
          time.sleep(1)
          cli =  SmsTcpClient( "cli", '127.0.0.1', 9999)   
          time.sleep(1)
          
          #cli.sendall('test')
          #msg = serv.recv(200)
          #print 'Serv.CpuTemp -> ' + cli.sm_func()
          print "-> RegName: " + cli.sm_func(cli.name, 'Serv.RegName', cli.name)
          print "-> CpuTemp: " + cli.sm_func(cli.name, 'Serv.CpuTemp', '.')
          print "-> Quit: " + cli.sm_func(cli.name, cli.name + '.Quit', cli.name) 
           
          self.assertEqual('ACK', cli.sm_func(cli.name, 'Serv.UnRegName', cli.name) )
          
          #cleanup_stop_thread();
          
          #cli.sendall('') # Stop server thread 
          cli.close()
          serv.close()
          self.assertEqual('test1', msg)
          
        
    print 3*'\n'
    print 70*'*'
    print 'Test: '
    unittest.main()
    

