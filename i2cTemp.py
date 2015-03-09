import smbus
import time

bus = smbus.SMBus(1)
address = 0x92 >> 1  # TempSens

def bearing255():
        bear = bus.read_byte_data(address, 1)
        return bear

def temp():
        bear1 = bus.read_byte_data(address, 0)
        bear2 = bus.read_byte_data(address, 0)
        bear = (bear2 << 8) + bear1
        bear = bear
        return bear

while True:

        print "T", temp()

        print bus.read_byte_data(address, 0), bus.read_byte_data(address, 1), bus.read_byte_data(address, 2), bus.read_byte_data(address, 3)  

        tmp = bus.read_word_data(address, 0)

        tmp = (0xff & tmp << 1) | (tmp >> 15) 
        print "W", tmp / 2.0
 
        time.sleep(1)
