from xr_i2c import I2c
import time

i2c = I2c()

class Hand:
    def __init__(self):
        pass

    def base_state(self):
        send = [0xff, 0x01, 0x01, 170, 0xff]
        send1 = [0xff, 0x01, 0x02, 45, 0xff]
        send4 = [0xff, 0x01, 0x04, 45, 0xff]
        send5 = [0xff, 0x01, 0x05, 100, 0xff]
        i2c.writedata(i2c.mcu_address, send)
        i2c.writedata(i2c.mcu_address, send1)
        i2c.writedata(i2c.mcu_address, send4)
        i2c.writedata(i2c.mcu_address, send5)
        time.sleep(1)

