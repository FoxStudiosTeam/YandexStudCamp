import time

from python_src.xr_car_light import Car_light, i2c
from python_src.xr_config import COLOR


class CustomLight(Car_light):
    def __init__(self):
        super().__init__()

    def set_led(self, num, color):
        group = 2  # Color car, not raspberry
        sendbuf = [0xff, group, num, COLOR.get(color), 0xff]
        i2c.writedata(i2c.mcu_address, sendbuf)
        time.sleep(0.005)

    def run(self):
        i = 0  # lamp num cant be more that 7 and less that 0
        j = 7

        while True:

            self.set_led(num=i, color=2)
            self.set_led(num=j, color=8)

            i += 1
            j -= 1

            if i > 7 or i < 0:
                i = 0

            if j < 0 or j > 7:
                j = 7
            time.sleep(0.01)