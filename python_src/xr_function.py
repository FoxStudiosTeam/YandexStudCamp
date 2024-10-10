# coding:utf-8
# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Функции для распознавания камеры и движения машины
# @contact :
# @Time    : 2020/05/09
# @File    : xr_function.py
# @Software: PyCharm

from builtins import float, object, bytes

import time
import xr_config as cfg

from xr_socket import Socket
socket = Socket()

from xr_motor import RobotDirection
go = RobotDirection()

from xr_car_light import Car_light

car_light = Car_light()


class Function(object):
	def __init__(self):
		pass

	def linepatrol_control(self):
		"""
        Управление движением машины для следования по линии
        :return:
        """
		while cfg.CAMERA_MOD == 1:
			dx = cfg.LINE_POINT_TWO - cfg.LINE_POINT_ONE  # Разность центрального положения верхней и нижней точек
			mid = int((cfg.LINE_POINT_ONE + cfg.LINE_POINT_TWO) / 2)  # Среднее положение центрального положения верхней и нижней точек

			print("dx==%d" % dx)  # Печать разности центрального положения верхней и нижней точек
			print("mid==%s" % mid)  # Печать среднего положения центрального положения верхней и нижней точек

			if 0 < mid < 260:  # Если центр линии смещен влево, значит машина отклонена вправо от траектории, необходимо повернуть влево для корректировки
				print("turn left")
				go.left()
			elif mid > 420:  # Если центр линии смещен вправо, значит машина отклонена влево от траектории, необходимо повернуть вправо для корректировки
				print("turn right")
				go.right()
			else:  # Если центр линии находится посередине
				if dx > 45:  # Если линия имеет тенденцию к правому наклону
					print("turn left")
					go.left()
				elif dx < -45:  # Если линия имеет тенденцию к левому наклону
					print("turn right")
					go.right()
				else:  # Если линия находится в вертикальном положении
					print("go stright")
					go.forward()
			time.sleep(0.007)
			go.stop()
			time.sleep(0.007)

	def qrcode_control(self):
		"""
        Управление движением машины для распознавания QR-кодов
        :return:
        """
		cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранение текущего значения скорости
		cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
		cfg.LEFT_SPEED = 30  # Установка подходящей скорости
		cfg.RIGHT_SPEED = 30
		code_status = 0
		while cfg.CAMERA_MOD == 4:
			time.sleep(0.05)
			if cfg.BARCODE_DATE == 'start':  # Проверка начала сигнала, проверка QR-кода 'start'
				# print(cfg.BARCODE_DATE)
				buf = bytes([0xff, 0x13, 0x0a, 0x00, 0xff])
				socket.sendbuf(buf)
				# cfg.LIGHT_STATUS = cfg.TURN_FORWARD
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['blue'])
				time.sleep(1.5)
				code_status = 1  # code_status
			elif cfg.BARCODE_DATE == 'stop':  # Проверка окончания сигнала, проверка QR-кода 'stop'
				# print(cfg.BARCODE_DATE)
				buf = bytes([0xff, 0x13, 0x0a, 0x01, 0xff])
				socket.sendbuf(buf)
				# cfg.LIGHT_STATUS = cfg.STOP
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['white'])
				time.sleep(1.5)
				code_status = 0  # code_status

			if code_status:
				if cfg.BARCODE_DATE == 'forward':  # Проверка QR-кода 'forward', движение машины вперед
					# print("forward")
					buf = bytes([0xff, 0x13, 0x0a, 0x02, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_FORWARD
					go.forward()
					time.sleep(2.5)
					go.stop()
					time.sleep(0.5)
				elif cfg.BARCODE_DATE == 'back':  # Проверка QR-кода 'back', движение машины назад
					# print("back")
					buf = bytes([0xff, 0x13, 0x0a, 0x03, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_BACK
					go.back()
					time.sleep(2.5)
					go.stop()
					time.sleep(0.5)
				elif cfg.BARCODE_DATE == 'left':  # Проверка QR-кода 'left', поворот машины влево
					# print("left")
					buf = bytes([0xff, 0x13, 0x0a, 0x04, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_LEFT
					go.left()
					time.sleep(1.5)
					go.stop()
					time.sleep(0.5)
				elif cfg.BARCODE_DATE == 'right':  # Проверка QR-кода 'right', поворот машины вправо
					# print("right")
					buf = bytes([0xff, 0x13, 0x0a, 0x05, 0xff])
					socket.sendbuf(buf)
					cfg.LIGHT_STATUS = cfg.TURN_RIGHT
					go.right()
					time.sleep(1.5)
					go.stop()
					time.sleep(0.5)
				else:
					# print("go.forward")
					cfg.LIGHT_STATUS = cfg.STOP
					# go.forward()
			else:
				go.stop()
				time.sleep(0.05)
		go.stop()
