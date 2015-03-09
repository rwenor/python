#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl

data = []
i = 0
with open('temp.dat', 'r') as f:
    for line in f:
        i = i + 1
        if i < 3:
            continue
        l = line.strip().split('\t')
        #print l
        data.append( float( l[2] ))
        
#print data

pl.plot(data)
pl.xlabel('x')
pl.ylabel('y')
# pl.xlim(0.0, 10.)
pl.show()

#data=np.genfromtxt('test.csv', dtype='i4,i2,i2,S3,S3,S3', names='Y,M,D,A,B,C')
