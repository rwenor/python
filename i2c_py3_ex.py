#!/usr/bin/env python3
import quick2wire.i2c as i2c

import time

address = 0x49

with i2c.I2CBus() as bus:
	bus.transaction(i2c.write_bytes(address, 0x01, 0x60))
	bus.transaction(i2c.write_bytes(address, 0x01))
	while True:
		

		sensora, sensorb = bus.transaction(i2c.write_bytes(address, 0x00),
		i2c.read(address, 2))[0]
		
		temp = (sensora << 8 | sensorb) / 256.
		
		print ("%02.02f" % temp)
		
		time.sleep(1)

