import socket
import sys
import time
import os
import threading
import subprocess


PrintTimeDiffLast = time.time()
PrintTimeCnt = 0

def PTD(str):
    global PrintTimeDiffLast
    global PrintTimeCnt
    print 'PTD%4s: %6s - %s' %  (PrintTimeCnt, \
                               int((time.time() - PrintTimeDiffLast)*1000), \
                               str) 
    PrintTimeCnt += 1
    PrintTimeDiffLast = time.time()



def sm_add(fra, til, data):
    try:
        d = data.strip().split(' ')

        dsum = 0
        for val in d:
            dsum += float(val)
        data = str(dsum)

    except:
        print '!X ' + data
        data = 'NAK'

    return data


def sm_ls(fra, til, data):
    try:
        subprocess.call(['ls', '-1'], shell=True)
        data = 'ACK'
    except:
        print '!X ' + data
        data = 'NAK'

    return data


def sm_print(fra, til, data):
    try:
        print "PRINT: " + data
        data = None
    except:
        print '!X ' + data
        data = 'NAK'

    return data
    
def sm_getCpuTemp(fra, til, data):
    try:
        res = os.popen('vcgencmd measure_temp').readline()
        data = res.replace("temp=","").replace("'C\n","")
         
        #data = '-999'    
    except:
        data = 'NAK'

    return data



def Disp_sm_pi(fra, til, data, con):

    print '*'*10
    print til
    to = til.pop(0)
    print to
    if to == 'Add':
        data = sm_add(fra, til, data)
    elif to == 'CpuTemp':
        data = sm_getCpuTemp(fra, til, data)
    elif to == 'ls':
        data = sm_ls(fra, til, data)
    elif to == 'Print':
        data = sm_print(fra, til, data)

    else:
        data = 'NAK'

    print data
    return data
    
def sms_pop(adr):
    return adr.pop(0), adr
    
    
    
## Test    
import unittest

class TestStringMethods(unittest.TestCase):

  def test_sms_pop(self):
      foo, rest = sms_pop('foo.rest.1'.split('.'))
      self.assertEqual('foo', foo)
      self.assertEqual(['rest', '1'], rest)
      
  def test_add(self):
      data = sm_add('', '', '1 2 3')
      self.assertEqual(data, '6.0')

  def _test_ls(self):
      data = sm_ls('', '', '1 2 3')
      self.assertEqual(data, 'ACK')

  def test_disp(self):
      data = Disp_sm_pi('Fra', 'Add'.split('.'), '1 2 3', None)
      self.assertEqual(data, '6.0')


if __name__ == '__main__':
  
    print 3*'\n'
    print 70*'*'
    print 'Test: '
    unittest.main()
