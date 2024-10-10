# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Модуль для управления питанием машины
# @Time    : 2020/05/09
# @File    : xr_power.py
# @Software: PyCharm

import time
from builtins import hex, bytes

from xr_i2c import I2c

i2c = I2c()

from xr_car_light import Car_light
rgb = Car_light()

import xr_config as cfg


class Power():
	def __init__(self):
		pass

	def got_vol(self):
		"""
        Получение информации о напряжении батареи
        :return:
        """
		time.sleep(0.005)
		vol_H = i2c.readdata(i2c.mcu_address, 0x05)  # Чтение обратной связи MCU о напряжении батареи, высокие 8 бит
		if vol_H is None:
			vol_H = 0
		time.sleep(0.005)
		vol_L = i2c.readdata(i2c.mcu_address, 0x06)  # Чтение обратной связи MCU о напряжении батареи, низкие 8 бит
		if vol_L is None:
			vol_L = 0
		vol = ((vol_H << 8) + vol_L)  # Комбинация высоких и низких 8 бит, усиление напряжения батареи в 100 раз
		return vol  # Возврат напряжения батареи

	# def show_vol(self, socket):
	def show_vol(self):
		"""
        Отображение уровня заряда батареи с помощью RGB-лампы
        :return:
        """
		vol = self.got_vol()
		if 370 < vol < 430 or 760 < vol < 860 or 1120 < vol < 1290:  # 70-100%, 8 светодиодов зеленого цвета
			rgb.set_ledgroup(cfg.POWER_LIGHT, 8, cfg.COLOR['green'])  # Установка лампы питания на зеленый цвет
			cfg.POWER = 3  # Установка уровня заряда батареи на 3
		elif 350 < vol < 370 or 720 < vol < 770 or 1080 < vol < 1120:  # 30-70%, 6 светодиодов оранжевого цвета
			rgb.set_ledgroup(cfg.POWER_LIGHT, 6, cfg.COLOR['orange'])
			cfg.POWER = 2  # Установка уровня заряда батареи на 2
		elif 340 < vol < 350 or 680 < vol < 730 or 1040 < vol < 1080:  # 10-30%, 2 светодиода красного цвета
			rgb.set_ledgroup(cfg.POWER_LIGHT, 2, cfg.COLOR['red'])
			cfg.POWER = 1  # Установка уровня заряда батареи на 1
		elif vol < 340 or vol < 680 or vol < 1040:  # <10%, 1 светодиод красного цвета
			rgb.set_ledgroup(cfg.POWER_LIGHT, 1, cfg.COLOR['red'])
			cfg.POWER = 0  # Установка уровня заряда батареи на 0