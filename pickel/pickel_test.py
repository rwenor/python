try:
    import cPickle as pickle
    print cPickle
except:
    import pickle
import pprint

data = [ { 'a':'A', 'b':2, 'c':3.0 } ]
print 'DATA:',
pprint.pprint(data)

data_string = pickle.dumps(data)
print 'PICKLE:', data_string


data2 = pickle.loads(data_string)
print 'DATA2:',
print data2
pprint.pprint(data2)