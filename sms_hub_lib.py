import socket
import sys
import time
import os
import threading
from sms_pi import *


conDict = {}



def Disp_sm_serv(fra, til, data, con):

    if til[0] == 'UnRegName':
        del conDict[data]
        data = 'ACK'
    elif til[0] == 'RegName':
        conDict[data] = sms_client(data, '', con)
        data = 'ACK'        
    else:
        data = Disp_sm_pi(fra, til, data, con)
            
    return data
    
    
def Disp_sm(fra, til, data, con):
  
    tlist = til.split('.')
    to = tlist.pop(0)
    
    #print 'YYYYYY'
    if to == 'Serv':
        data = Disp_sm_serv(fra, tlist, data, con)
        
    elif to in conDict:
        to_sm = conDict[to]
        msg = fra + '\t' + til + '\t' + data
        print '<< "' + msg + '" --> ' + to_sm.cName
        to_sm.con.sendall(msg)
        #data = Disp_sm_pi(fra, til, data, con)
        data = None
    else:
        data = 'No srv: '+ to
            
    return data

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
  

## Test    
import unittest

class TestStringMethods(unittest.TestCase):

  def test_RegName(self):
      data = Disp_sm_serv('Fra 1', 'RegName'.split('.'), 'Fra 1', test_con('Fra 1', '1.2.3.4', 1))
      self.assertEqual(data, 'ACK')
      print conDict

  def test_Disp(self):
      data = Disp_sm('Test.Fra 1', 'Serv.RegName', 'Fra 1', test_con('Fra 1', '1.2.3.4', 1))
      self.assertEqual(data, 'ACK')
      print conDict

  def test_Disp_Send(self):
      # Setup
      data = Disp_sm('Test.Fra 1', 'Serv.RegName', 'Fra 1', test_con('Fra 1', '1.2.3.4', 1))
      self.assertEqual(data, 'ACK')
      print conDict
      
      # Send
      data = Disp_sm('Test.Fra 1', 'Fra 1.Test', 'Data', '')
      self.assertEqual(data, None)
      print conDict
      

def con_recv(con, addr):
    try:
        print >>sys.stderr, 'connection from', addr
        
        while True:
            data = con.recv(200)
            
            if data:
                l = data.strip().split('\t')
                print >>sys.stderr, '>> "%s"' % str(len(l)) + ' : ' + data
                if len(l) < 4:
                    print "Err: ", l
                    if len(l) > 2:
                        l[2] = 'Err to long?'
                    else:
                        continue
                    
                else:
                    l[2] = Disp_sm(l[0], l[1], l[2], con)

                #print >>sys.stderr, 'sending data back to the client'
                if l[2] <> None:
                    data = l[1] + '\t' + l[0] + '\t' + l[2]
                    con.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', addr
                break
            
    finally:      
        # Clean up the connection
        con.close()
    
      

if __name__ == '__main__':
  
    print 3*'\n'
    print 70*'*'
    print 'Test: '
    unittest.main()
    

