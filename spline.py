from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import random

x = np.linspace(0, 10, num=21, endpoint=True)
y = np.cos(-x**2/9.0) 
noise = np.random.normal(0,0.2,21)
y = y + noise
y0 = np.cos(-x**2/9.0)
print x
print y

f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(0, 10, num=101, endpoint=True)

plt.plot(x, y0, 'o', x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()
