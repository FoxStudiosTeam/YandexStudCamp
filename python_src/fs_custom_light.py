import time

from xr_car_light import Car_light, i2c
from xr_config import COLOR


class CustomLight(Car_light):
    def __init__(self):
        super().__init__()

    def set_led(self, num, color):
        group = 2  # Color car, not raspberry
        sendbuf = [0xff, group, num, COLOR[color], 0xff]
        i2c.writedata(i2c.mcu_address, sendbuf)
        time.sleep(0.005)

    def run(self):
        i = 0  # lamp num cant be more that 7 and less that 0
        j = 7

        while True:
            self.set_ledgroup(1,8,COLOR['red'])
            # self.set_led(num=j, color='black')
            # self.set_led(num=i, color='orange')

            # i += 1

            # if i > 7 or i < 0:
            #     i = 0
            #     j = 7

            # if i < 8 and i > 0:
            #     j = i-1
            time.sleep(0.01)