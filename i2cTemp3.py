import smbus
import time

bus = smbus.SMBus(1)
address = 0x92 >> 1  # TempSens MCP9800

def readTemp9b():
        tmp1 = bus.read_word_data(address, 0)
        print "9b", tmp1
        tmp1 = (0xff & tmp1 << 1) | (tmp1 >> 15)
        return tmp1 / 2.0

def readTemp12b():
        tmp1 = bus.read_word_data(address, 0)
        print "12b", tmp1, ", Bin: ", bin(0xff00 & tmp1), bin(0xff & tmp1) 
        #tmp1 = (c << 4) | (tmp1 >> 12)
        return (0xff & tmp1) + (tmp1 >> 12) / 16.0

def tempSet12b():
        print "c:", bus.read_byte_data(address, 1)
        bus.write_byte_data(address, 0x01, 0x60)
        print "c:", bus.read_byte_data(address, 1)

for i in range(0, 6):
        print "Temp:", i, readTemp9b()
        time.sleep(1)


tempSet12b()
for i in range(0, 60):
        print "Temp:", i, readTemp12b()
        time.sleep(1)
