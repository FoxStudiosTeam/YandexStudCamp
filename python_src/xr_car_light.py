# coding:utf-8
# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Функции для фар автомобиля
# @contact :
# @Time    : 2020/05/09
# @File    : xr_car_light.py
# @Software: PyCharm

from builtins import int, range
import xr_config as cfg

import time
from xr_i2c import I2c

i2c = I2c()


class Car_light(object):
	def __init__(self):
		pass

	def set_led(self, group, num, color):
		"""
        Установка состояния светодиодов RGB
        :param group: группа светодиодов, равна 1 для индикаторов заряда батареи, 2 для фар автомобиля
        :param num: индекс светодиода
        :param color: устанавливаемый цвет, в конфигурации COLOR можно выбрать соответствующий цвет, допустимо установить только определенные цвета
        :return:
        """
		if 0 < num < 9 and 0 < group < 3 and color < 9:
			sendbuf = [0xff, group + 3, num, color, 0xff]
			i2c.writedata(i2c.mcu_address, sendbuf)
			time.sleep(0.005)
		# print("set_led group%d, LED%d, color%d  :OK \r\n", group, num, color)

	def set_ledgroup(self, group, count, color):
		"""
        Установка состояния группы светодиодов RGB
        :param group: группа светодиодов, равна 1 для индикаторов заряда батареи, 2 для фар автомобиля
        :param count: количество светодиодов
        :param color: устанавливаемый цвет, в конфигурации COLOR можно выбрать соответствующий цвет, допустимо установить только определенные цвета
        :return:
        """
		if 0 < count < 9 and 0 < group < 3 and color < 9:
			sendbuf = [0xff, group + 1, count, color, 0xff]
			i2c.writedata(i2c.mcu_address, sendbuf)
			time.sleep(0.005)
		# print("set_led group%d, LED%d, color%d  :OK \r\n", group, count, color)

	def open_light(self):
		"""
        Включить все фары автомобиля
        :return:
        """
		# print("车灯全部打开")
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['white'])
		time.sleep(0.01)

	def close_light(self):
		"""
        Выключить все фары автомобиля
        :return:
        """
		# print("车灯全部关闭")
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		time.sleep(0.01)

	def left_turn_light(self):
		"""
        Левый поворотный свет
        :return:
        """
		# print("左转")
		self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 7, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 8, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		time.sleep(0.12)

	def right_turn_light(self):
		"""
        Правый поворотный свет
        :return:
        """
		self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 2, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_led(cfg.CAR_LIGHT, 1, cfg.COLOR['red'])
		time.sleep(0.12)
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		time.sleep(0.12)

	def forward_turn_light(self):
		self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['green'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 4, cfg.COLOR['green'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 5, cfg.COLOR['green'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['green'])
		time.sleep(0.12)

	def back_turn_light(self):
		self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['red'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 4, cfg.COLOR['red'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 5, cfg.COLOR['red'])
		time.sleep(0.05)
		self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['red'])
		time.sleep(0.12)

	def init_led(self):
		"""
        Инициализация светового режима автомобиля
        :return:
        """
		self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
		for j in range(8):
			for i in range(8):
				self.set_led(cfg.CAR_LIGHT, i + 1, j + 1)
				time.sleep(0.05)
				self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
				time.sleep(0.05)

			for i in range(4):
				self.set_led(cfg.CAR_LIGHT, i + 1, j + 1)
				self.set_led(cfg.CAR_LIGHT, 8 - i, j + 1)
				time.sleep(0.05)

			for i in range(4):
				self.set_led(cfg.CAR_LIGHT, i + 1, cfg.COLOR['black'])
				self.set_led(cfg.CAR_LIGHT, 8 - i, cfg.COLOR['black'])
				time.sleep(0.05)