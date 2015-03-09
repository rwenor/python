import smbus
import time

bus = smbus.SMBus(1)
address = 0x9A >> 1  # TempSens

def bearing255():
        bear = bus.read_byte_data(address, 1)
        return bear

def temp():
        bear1 = bus.read_byte_data(address, 0)
        bear2 = bus.read_byte_data(address, 1)
        bear = (bear1 << 8) + bear2
        bear = bear/1000.0
        return bear

while True:

        print temp()
        time.sleep(1)
