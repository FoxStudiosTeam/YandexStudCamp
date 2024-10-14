from xr_i2c import I2c
import time

i2c = I2c()

class Hand:
    def __init__(self):
        pass

    def test_move(self):
        send = [0xff, 0x01, 0x01, 145, 0xff]
        i2c.writedata(i2c.mcu_address, send)
        time.sleep(1)