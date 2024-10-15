from xr_i2c import I2c
from xr_servo import Servo
import time

i2c = I2c()


class Hand(Servo):
    def __init__(self):
        pass

    # def base_state(self):
    #     needSend = [
    #         [0xff, 0x01, 0x01, 170, 0xff],
    #         [0xff, 0x01, 0x02, 45, 0xff],
    #         [0xff, 0x01, 0x03, 90, 0xff],
    #         [0xff, 0x01, 0x04, 120, 0xff],
    #         [0xff, 0x01, 0x05, 100, 0xff],
    #         [0xff, 0x01, 0x06, 130, 0xff],
    #         [0xff, 0x01, 0x07, 140, 0xff],
    #         [0xff, 0x01, 0x08, 150, 0xff],
    #     ]
    #     j = 1
    #     for i in needSend:
    #         i2c.writedata(i2c.mcu_address, i)
    #         #print(f'Угол серво №{j} ({i[2]}) = ', i[3])
    #         #j = j+1
    #     print(i2c.readdata(i2c.mcu_address, 0x01))
    #     time.sleep(1)
    
    def test_state(self):
        self.set(1, 150)
        self.set(2, 45)
        self.set(3, 45)
        self.set(4, 15)
        self.set(5, 50)
        self.set(6, 50)
