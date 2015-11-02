#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd    
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
		print 'Må ha en fil å jobbe med...'
		exit()
	
fName = sys.argv[1]
i = 0
with open(fName) as f:
    for line in f:
    		i += 1
    		if line[:2] == '#H':
    			  plt.title( line[3:] )
    		elif line[:2] == '#1':
    			  s1l = line[3:] 
    		elif line[:2] == '#2':
    			  s2l = line[3:]   
    		else:
    				print 'Ignored: ', i, line[:-1]
    				
    		if i == 5:
    			  break
    			  
    	
        

df =  pd.read_csv(fName, sep=',', skiprows=5, names=['x','s1','s2'])

plt.plot(df.s1, label=s1l)
plt.plot(df.s2, label=s2l)
plt.legend()
plt.show()

