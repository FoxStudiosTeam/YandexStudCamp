from xr_i2c import I2c
import time

i2c = I2c()


class Hand:
    def __init__(self):
        pass

    def base_state(self):
        needSend = [
            [0xff, 0x01, 0x01, 170, 0xff],
            [0xff, 0x01, 0x02, 45, 0xff],
            [0xff, 0x01, 0x03, 90, 0xff],
            [0xff, 0x01, 0x04, 120, 0xff],
            [0xff, 0x01, 0x05, 100, 0xff],
            [0xff, 0x01, 0x06, 130, 0xff],
            [0xff, 0x01, 0x07, 140, 0xff],
            [0xff, 0x01, 0x08, 150, 0xff],
        ]
        j = 1
        for i in needSend:
            i2c.writedata(i2c.mcu_address, i)
            print(f'Угол угла серво №{j} ({i[2]}) = ', i[3])
            j = j+1
        time.sleep(1)
