# coding:utf-8

# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!
"""
@version: python3.7
@Author  : xiaor
@Explain :PS2手柄模块
@Time    :2020/05/09
@File    :xr_ps2.py
@Software: PyCharm
"""
import time
import xr_config as cfg
from xr_i2c import I2c
from fs_move_hand import Hand

hand = Hand()

i2c = I2c()

from xr_motor import RobotDirection

go = RobotDirection()

from xr_servo import Servo
servo = Servo()

class PS2(object):
	def __init__(self):
		pass

	def ps2_button(self):
		"""
        Получение состояния кнопок PS2-джойстика
        :return: Значение кнопки после декодирования cfg.PS2_READ_KEY
        """
		ps2check = i2c.readdata(i2c.ps2_address, 0x01)  # Получение возвращаемого PS2 режима
		read_key = i2c.readdata(i2c.ps2_address, 0x03)  # Получение возвращаемых PS2 значений кнопок
		read_key1 = i2c.readdata(i2c.ps2_address, 0x04)  # Получение возвращаемых PS2 значений кнопок
		cfg.PS2_READ_KEY = 0
		if ps2check == 0x41 or ps2check == 0xC1 or ps2check == 0x73 or ps2check == 0xF3:  # Обычный режим PS2
			if read_key == 0xef:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_UP']
			elif read_key == 0xbf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_DOWN']
			elif read_key == 0xcf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_LEFT']
			elif read_key == 0xdf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_RIGHT']
			elif read_key1 == 0xef:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_GREEN']
			elif read_key1 == 0xbf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_BLUE']
			elif read_key1 == 0xcf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PINK']
			elif read_key1 == 0xdf:
				cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_RED']
		return cfg.PS2_READ_KEY

	def control(self):
		"""
        Функция управления через джойстик PS2
        :return:
        """
		read_ps2 = self.ps2_button()  # Получение значения кнопки
		add = 5
		if cfg.PS2_LASTKEY != read_ps2 and cfg.PS2_LASTKEY != 0:  # Если значение предыдущей кнопки не равно 0 и отличается от текущего значения, это означает изменение значения кнопки и оно не равно 0
			go.stop()  # При изменении значения кнопки выполнить однократную остановку
			cfg.LIGHT_STATUS = cfg.STOP  # Установить статус кнопки на остановку
			cfg.PS2_LASTKEY = 0  # Установить предыдущий статус равным нулю, чтобы избежать повторного входа и остановки

		else:
			if read_ps2 == cfg.PS2_KEY['PSB_PAD_UP']:  # Равно левой кнопке вверх
				go.forward()
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2  # Обновить последнее значение

			elif read_ps2 == cfg.PS2_KEY['PSB_PAD_DOWN']:  # Равно левой кнопке вниз
				go.back()
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2

			elif read_ps2 == cfg.PS2_KEY['PSB_PAD_LEFT']:  # Равно левой кнопке влево
				go.left()
				cfg.LIGHT_STATUS = cfg.TURN_LEFT
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2

			elif read_ps2 == cfg.PS2_KEY['PSB_PAD_RIGHT']:  # Равно левой кнопке вправо
				go.right()
				cfg.LIGHT_STATUS = cfg.TURN_RIGHT
				time.sleep(0.02)
				cfg.PS2_LASTKEY = read_ps2

			if read_ps2 == cfg.PS2_KEY['PSB_RED']:  # Равно красной кнопке
				hand.push_button()
				time.sleep(0.5)
				hand.normal_state()
				cfg.PS2_LASTKEY = read_ps2

			elif read_ps2 == cfg.PS2_KEY['PSB_PINK']:  # Равно розовой кнопке
				# print('PSB_BLUE')
				hand.catch_cube()
				cfg.PS2_LASTKEY = read_ps2

			elif read_ps2 == cfg.PS2_KEY['PSB_GREEN']:  # Равно зеленой кнопке
				# print('PSB_GREEN')
				hand.drop()
				hand.normal_state()
				cfg.PS2_LASTKEY = read_ps2

			elif read_ps2 == cfg.PS2_KEY['PSB_BLUE']:  # Равно синей кнопке
				# print('PSB_PINK')
				hand.catch_sphere()
				cfg.PS2_LASTKEY = read_ps2