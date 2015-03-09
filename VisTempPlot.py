#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl
# Use numpy to load the data contained in the file

data=np.loadtxt('/home/pi/Python/temp.dat', skiprows=30,
        dtype=[('f0',str),('f1',str),('f2',float),('f3',str),('f4',str)])

print data


data=np.loadtxt('/home/pi/Python/xy.dat')

print data
print data[:,1]


# plot the first column as x, and second column as y
#pl.plot(data)
pl.plot(data[:,0], data[:,1])
pl.xlabel('x')
pl.ylabel('y')
# pl.xlim(0.0, 10.)
pl.show()
