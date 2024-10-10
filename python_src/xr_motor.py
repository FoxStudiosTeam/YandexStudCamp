# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Управление двигателями
# @contact :
# @Time    : 2020/05/09
# @File    : xr_motor.py
# @Software: PyCharm

from builtins import float, object

import os
import xr_gpio as gpio
import xr_config as cfg

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)


class RobotDirection(object):
	def __init__(self):
		pass

	def set_speed(self, num, speed):
		"""
		Установка скорости двигателя, num указывает на левую или правую сторону, 1 - левая, 2 - правая, speed - установленное значение скорости (0-100)
		"""
		# print(speed)
		if num == 1:  # Регулировка левой стороны
			gpio.ena_pwm(speed)
		elif num == 2:  # Регулировка правой стороны
			gpio.enb_pwm(speed)

	def motor_init(self):
		"""
		Получение сохраненной скорости робота
		"""
		print("Получение сохраненной скорости робота")
		speed = cfgparser.get_data('motor', 'speed')
		cfg.LEFT_SPEED = speed[0]
		cfg.RIGHT_SPEED = speed[1]
		print(speed[0])
		print(speed[1])

	def save_speed(self):
		speed = [0, 0]
		speed[0] = cfg.LEFT_SPEED
		speed[1] = cfg.RIGHT_SPEED
		cfgparser.save_data('motor', 'speed', speed)

	def m1m2_forward(self):
		# Установка двигателей M1 и M2 на прямую передачу
		gpio.digital_write(gpio.IN1, True)
		gpio.digital_write(gpio.IN2, False)

	def m1m2_reverse(self):
		# Установка двигателей M1 и M2 на реверсную передачу
		gpio.digital_write(gpio.IN1, False)
		gpio.digital_write(gpio.IN2, True)

	def m1m2_stop(self):
		# Установка двигателей M1 и M2 на остановку
		gpio.digital_write(gpio.IN1, False)
		gpio.digital_write(gpio.IN2, False)

	def m3m4_forward(self):
		# Установка двигателей M3 и M4 на прямую передачу
		gpio.digital_write(gpio.IN3, True)
		gpio.digital_write(gpio.IN4, False)

	def m3m4_reverse(self):
		# Установка двигателей M3 и M4 на реверсную передачу
		gpio.digital_write(gpio.IN3, False)
		gpio.digital_write(gpio.IN4, True)

	def m3m4_stop(self):
		# Установка двигателей M3 и M4 на остановку
		gpio.digital_write(gpio.IN3, False)
		gpio.digital_write(gpio.IN4, False)

	def forward(self):
		"""
		Установка направления движения робота вперед
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_forward()

	def back(self):
		"""
		Установка направления движения робота назад
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_reverse()

	def left(self):
		"""
		Установка направления движения робота влево
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_forward()

	def right(self):
		"""
		Установка направления движения робота вправо
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_reverse()

	def stop(self):
		"""
		Установка направления движения робота на остановку
		"""
		self.set_speed(1, 0)
		self.set_speed(2, 0)
		self.m1m2_stop()
		self.m3m4_stop()
