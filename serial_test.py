import serial
#from serial import serial

def prt_dict(d):
    print "NMEA:"
    for s in d:
        print d[s]

def nmea_pos(d):
    return d['$GNGLL'][2] + d['$GNGLL'][1][:2] +' '+ d['$GNGLL'][1][2:] \
        +' '+ d['$GNGLL'][4] + d['$GNGLL'][3][:3] +' '+ d['$GNGLL'][3][3:]

ser = serial.Serial(port='COM3', baudrate=9600)

print("connected to: " + ser.portstr)
count=1
str = ""
d = {}

while True:
    for line in ser.read():
        
        if not ord(line) in (10,13):
            str += line
            
        if ord(line) == 13:
            if str[:1] == '$' :
                d[str[:6]] = str.split(',')
            if '$GNGLL' == str[:6]:
                print nmea_pos(d)
                
            str = ''
            
        count = count+1
        
    #print count    
    if count > 10000:
        print "break"
        break
        

    
prt_dict(d)
ser.close()