import socket
import sys
import time
import os
import threading


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

        data = 0
        for val in d:
            data += float(val)
        data = str(data)

    except:
        data = 'ERR'

    return data

    
def sm_getCpuTemp(fra, til, data):
    try:
        res = os.popen('vcgencmd measure_temp').readline()
        data = res.replace("temp=","").replace("'C\n","")
            
    except:
        data = 'ERR'

    return data



def Disp_sm_pi(fra, til, data, con):

    if til == 'Til.Add':
        data = sm_add(fra, til, data)
    elif til == 'Til.CpuTemp':
        data = sm_getCpuTemp(fra, til, data)

    else:
        data = 'ERR'

    return data
    

