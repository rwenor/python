import matplotlib.pyplot as plt
from functools import partial
import multiprocessing

import time
# Test og mer 
 
 
def mandelbrotCalcRow(yPos, h, w, max_iteration = 1000):
    y0 = yPos * (2/float(h)) - 1 #rescale to -1 to 1
    row = []
    for xPos in range(w):
        x0 = xPos * (3.5/float(w)) - 2.5 #rescale to -2.5 to 1
        iteration, z = 0, 0 + 0j
        c = complex(x0, y0)
        while abs(z) < 2 and iteration < max_iteration:
            z = z**2 + c
            iteration += 1
        row.append(iteration)
 
    return row

 
def mandelbrotCalcSet(h, w, max_iteration = 1000):
    partialCalcRow = partial(mandelbrotCalcRow, h=h, w=w, max_iteration = max_iteration)
    mandelImg = map(partialCalcRow, xrange(h))
    return mandelImg


def mandelbrotCalcSetMulti(h, w, max_iteration = 1000):
    #make a helper function that better supports pool.map by using only 1 var
    #This is necessary since the version
    partialCalcRow = partial(mandelbrotCalcRow, h=h, w=w, max_iteration = max_iteration)
 
    pool =multiprocessing.Pool() #creates a pool of process, controls worksers
    #the pool.map only accepts one iterable, so use the partial function
    #so that we only need to deal with one variable.
    mandelImg = pool.map(partialCalcRow, range(h)) #make our results with a map call
    pool.close() #we are not adding any more processes
    pool.join() #tell it to wait until all threads are done before going on
 
    return mandelImg
 

if __name__=='__main__':
	t0 = time.time()
	mandelImg = mandelbrotCalcSetMulti(800, 800, 20)
	print( time.time() - t0)

	plt.imshow(mandelImg)
	plt.savefig('mandelimg.jpg')
