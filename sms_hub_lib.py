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
    else:
        to_sm = conDict[to]
        msg = fra + '\t' + til + '\t' + data
        #print msg, to_sm.con.con
        to_sm.con.sendall(msg)
        #data = Disp_sm_pi(fra, til, data, con)
        data = None
            
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
      

if __name__ == '__main__':
  
    print 3*'\n'
    print 70*'*'
    print 'Test: '
    unittest.main()
    

