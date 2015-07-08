import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def Worker():
    print 'in'
    time.sleep(5)
    print 'out'

t = threading.Thread(target=Worker, args=())
#t.dameon = False
t.start()

t.join()
logging.debug('End')
ps
