import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

def read_datafile(file_name):
    # the skiprows keyword is for heading, but I don't know if trailing lines
    # can be specified
    data = np.loadtxt(file_name, delimiter=',', skiprows=10)
    return data

data = read_datafile('e:\dir1\datafile.csv')

x = ???
y = ???

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Mains power stability")    
ax1.set_xlabel('time')
ax1.set_ylabel('Mains voltage')

ax1.plot(x,y, c='r', label='the data')

leg = ax1.legend()

plt.show()