
print "Hei Cloud9 2"

startM = 18.00

##
# 0: dato
# 1: tid
# 2: tid  sec
# 3: avstand
# 4: avstand enhet
# 5:

class ParsLWStreem:
    def __init__(self, detV = (20.0, 15.0)):
        self.detV = detV  # Deteksjons vindu
        self.state = 0
        self.lastM = (0.0, 0.0)
        self.lnr = 0
        self.tick = 0.03
        self.vStart = 0
        
    def calcSpeed(self, newM):
        print self.state, newM, self.lastM
        if self.state == 1:
            self.lastM = newM
            return -1
        else:
            v = (newM[0] - self.lastM[0]) / (newM[1] - self.lastM[1]) * 3.6 # m/s*3600/1000
            self.lastM = newM
            return -v
            
        
    def parsline(self, line):
        self.lnr += 1
        
        dat = line.split()
        if dat[3] == '--.--':
            self.state = 0
            self.lastM = (0.0, 0.0)
            return -1
        
        if float(dat[3]) < self.detV[0]:
            self.state += 1
            
            print line  
            print self.calcSpeed((float(dat[3]), float(dat[2])))
            # for i, itm in enumerate(dat):
            #    print i, itm 
            
        else:
            self.state = 0
            self.lastM = (0.0, 0.0)
            return -1
        
        
wlPars = ParsLWStreem()


with open('temp.txt') as f:
    # print f.readlines()
    
    for line in f:
        wlPars.parsline(line.strip())