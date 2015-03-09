import smbus
import time

bus = smbus.SMBus(1)
address = 0x92 >> 1  # TempSens MCP9800

def readTemp9b():
        tmp1 = bus.read_word_data(address, 0)
        tmp1 = (0xff & tmp1 << 1) | (tmp1 >> 15)
        return tmp1 / 2.0

def tempSet12b():
        bear1 = bus.read_byte_data(address, 0)
        bear2 = bus.read_byte_data(address, 0)
        bear = (bear2 << 8) + bear1
        bear = bear
        return bear

while True:
        print "Temp:", readTemp9b()
 
#        time.sleep(1)
