#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
import sys, getopt
import datetime



def isodate(str):
        return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')

try:
        opts, args = getopt.getopt(sys.argv[1:], 's:p:d:', \
                                   ['tull=', 's=', 'param='])
except getopt.GetoptError as err:
        print str(err)
        print "Feil args"
        #usage()
        sys.exit(2)
        
#print opts
#print args
saveFile = ''
loadFile = 'TempLog.dat'
param = 'Ute'
param2 = 'Ute oppe'
humStart = 0
dayNr = 2

for o, a in opts:
    if o in ('-s', '--s'):
        saveFile = a
    elif o in ('-p', '--param'):
        param = a
        if a == "Bad":
            loadFile = "TempLog" + a + ".dat"
            param2 = "Bad - gulv"
            humStart = 20
    elif o in ('-d', '--days'):
        print a
        dayNr = int(a)

data1 = []
data2 = []
data3 = []
date1 = []
date2 = []
date3 = []

i = 0

with open(loadFile, 'r') as f:
    for line in f:
        i = i + 1
        if i < 3:
            continue
        l = line.strip().split('\t')
        
        if len(l) < 4:
            print "Line", i, ": ", l
            continue

        #print "xLine ", i, l, len(l)
        if l[0] == param:   # Bad eller Ute
            data1.append( float( l[2] ))
            date1.append( isodate( l[3] ) )
        
        if l[0] == param2:
            if l[1] == 'temp':
                data2.append( float( l[2] ))
                date2.append( isodate(l[3]) )
            else:
                data3.append( float( l[2] ) / 10.0 + humStart)
                date3.append( isodate(l[3]) )
                
#print data
#pl.figure(1)
#date1 = pl.dates.date2num(date1)
pl.xticks(rotation=70)
pl.plot_date(date1[-6*24*dayNr:], data1[-6*24*dayNr:], '-')
pl.plot_date(date2[-6*24*dayNr:], data2[-6*24*dayNr:], '-')
if param2 != "Bad - gulv":
    pl.plot_date(date3[-6*24*dayNr:], data3[-6*24*dayNr:], '-')

#print date2

#pl.plot(data1[-6*24*dayNr:])
#pl.plot(data2[-6*24*dayNr:])
#pl.plot(data3[-6*24*dayNr:])

#pl.fmt_xdata = DateFormatter('%Y-%m-%d')
pl.xlabel('x')
pl.ylabel('Temp / hum/10')
# pl.xlim(0.0, 10.)
pl.grid(color='r')

if saveFile <> '':
    pl.savefig(saveFile, dpi=110, bbox_inches='tight')   
else:
    pl.show()


#data=np.genfromtxt('test.csv', dtype='i4,i2,i2,S3,S3,S3', names='Y,M,D,A,B,C')
