#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
import sys, getopt


try:
        opts, args = getopt.getopt(sys.argv[1:], 's', ['tull=', 's='])
except getopt.GetoptError as err:
        print str(err)
        print "Feil args"
        #usage()
        sys.exit(2)
        
print opts
print args
saveFile = ''
for o, a in opts:
    if o == '-s':
        saveFile = args[0]
    elif o == '--s':
        saveFile = a
        

data1 = []
data2 = []
data3 = []

i = 0
#with open('temp.dat', 'r') as f:
with open('TempLog.dat', 'r') as f:
    for line in f:
        i = i + 1
        if i < 3:
            continue
        l = line.strip().split('\t')
        
        if len(l) < 3:
            print "Line", i, ": ", l
            continue

        #print "xLine ", i, l, len(l)
        if l[0] == 'Bad':
            data1.append( float( l[2] ))
        
        if l[0] == 'Bad - gulv':
            if l[1] == 'temp':
                data2.append( float( l[2] ))
            else:
                data3.append( float( l[2] ) / 10.0 + 20)
                
#print data
#pl.figure(1)
dagSamp = 6*24
samp = dagSamp*10
pl.plot(data1[:-samp])
pl.plot(data2[:-samp])
pl.plot(data3[:-samp])

pl.xlabel('x')
pl.ylabel('Temp / hum/10')
# pl.xlim(0.0, 10.)
pl.grid(color='r')

if saveFile <> '':
    pl.savefig(saveFile)   
else:
    pl.show()


#data=np.genfromtxt('test.csv', dtype='i4,i2,i2,S3,S3,S3', names='Y,M,D,A,B,C')
