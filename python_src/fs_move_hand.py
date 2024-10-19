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
    
    def normal_state(self):
        self.set(1,180)
        time.sleep(0.5)
        self.set(2, 30)
        self.set(3, 90)
        self.set(4, 90)
        self.set(7, 85)
        self.set(8, 105)

    def catch_cube(self):
        # 28см от машинки до кубика
        self.set(2, 180)
        time.sleep(0.2)
        self.set(1, 75)
        self.set(3, 90)
        self.set(4, 45)
        time.sleep(1)
        self.set(4, 85)
        self.set(1, 180)
        self.set(2, 90)

    def catch_sphere(self):
        # 28см от машинки до кубика
        self.set(2, 180)
        time.sleep(0.2)
        self.set(1, 75)
        self.set(3, 90)
        self.set(4, 45)
        time.sleep(1)
        self.set(4, 90)
        self.set(1, 180)
        self.set(2, 90)

    def drop(self):
        # корзинка должна быть в 10см
        self.set(2, 140)
        self.set(1, 130)
        self.set(3, 90)
        time.sleep(0.5)
        self.set(4, 45)
        time.sleep(1)        

    def push_button(self):
        self.set(2, 180)
        time.sleep(0.7)
        self.set(2, 70)
        time.sleep(0.7)
        self.set(2, 90)