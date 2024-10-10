# coding:utf-8
# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Модуль для работы с ультразвуковыми датчиками
# @Time    : 2020/05/09
# @File    : xr_ultrasonic.py
# @Software: PyCharm

import time
from builtins import int, chr, object

import xr_gpio as gpio
import xr_config as cfg

from xr_motor import RobotDirection
go = RobotDirection()

from xr_servo import Servo
servo = Servo()

from xr_socket import Socket
socket = Socket()


class Ultrasonic(object):
	def __init__(self):
		self.MAZE_ABLE = 0
		self.MAZE_CNT = 0
		self.MAZE_TURN_TIME = 0
		self.dis = 0
		self.s_L = 0
		self.s_R = 0

	def get_distance(self):
		"""
		Функция получения расстояния с ультразвукового датчика, возвращает расстояние в см
		"""
		time_count = 0
		time.sleep(0.01)
		gpio.digital_write(gpio.TRIG, True)  # Установить высокий уровень на выводе Trig
		time.sleep(0.000015)  # Послать импульс высокого уровня длительностью не менее 10 мкс
		gpio.digital_write(gpio.TRIG, False)  # Установить низкий уровень на выводе Trig
		while not gpio.digital_read(gpio.ECHO):  # Ждать, пока вывод Echo изменится с низкого на высокий уровень
			pass
		t1 = time.time()  # Записать начальный момент времени, когда Echo стал высоким
		while gpio.digital_read(gpio.ECHO):  # Ждать, пока вывод Echo станет низким
			if time_count < 2000:  # Проверка на тайм-аут, чтобы избежать бесконечного цикла
				time_count += 1
				time.sleep(0.000001)
				continue
			else:
				print("Нет приема ECHO! Пожалуйста, проверьте подключение")
				break
		t2 = time.time()  # Записать конечный момент времени, когда Echo стал низким
		distance = (t2 - t1) * 340 / 2 * 100  # Время между высокими уровнями - это время, которое требуется звуковому сигналу для прохождения туда и обратно, то есть время умножается на скорость звука и делится на два, чтобы получить одностороннее расстояние
		# Умножить результат на 100, чтобы преобразовать расстояние из метров в сантиметры
		# print("расстояние составляет %d" % distance) # Печатает расстояние
		if distance < 500:  # Нормальный диапазон измерений
			# print("расстояние составляет %d" % distance)
			cfg.DISTANCE = round(distance, 2)
			return cfg.DISTANCE
		else:
			# print("расстояние составляет 0") # Если расстояние больше 5 м, оно выходит за пределы диапазона измерения
			cfg.DISTANCE = 0
			return 0

	def avoidbyragar(self):
		"""
		  Функция избежания препятствий с использованием ультразвуковых датчиков
		  """
		cfg.LEFT_SPEED = 30
		cfg.RIGHT_SPEED = 30
		dis = self.get_distance()
		if 25 < dis < 300 or dis == 0:  # Расстояние больше 25 см и меньше 300 см или равно 0 (измерение за пределами диапазона)
			cfg.AVOID_CHANGER = 1
		else:
			if cfg.AVOID_CHANGER == 1:
				go.stop()
				cfg.AVOID_CHANGER = 0

	def send_distance(self):
		"""
		  Отправка данных о расстоянии до верхнего уровня
		  """
		dis_send = int(self.get_distance())
		# print(dis_send)
		if 1 < dis_send < 255:
			buf = bytes([0xff, 0x31, 0x02, dis_send, 0xff])  # Отправить расстояние до верхнего уровня
			try:
				socket.sendbuf(buf)
			except Exception as e:  # Ошибка отправки
				print('Ошибка отправки расстояния:', e)  # Отобразить сообщение об ошибке
		else:
			buf = []

	def maze(self):
		"""
		  Функция перемещения по лабиринту с использованием ультразвуковых датчиков
		  """
		cfg.LEFT_SPEED = 35
		cfg.RIGHT_SPEED = 35
		# print("Функция перемещения по лабиринту с использованием ультразвуковых датчиков")
		self.dis = self.get_distance()  # Получить расстояние
		if self.MAZE_ABLE == 0 and (
				(self.dis > 30) or self.dis == 0):  # Если перед машиной нет препятствий и она не в тупике
			while ((self.dis > 30) or self.dis == 0) and cfg.CRUISING_FLAG:
				self.dis = self.get_distance()
				go.forward()
			if cfg.CRUISING_FLAG:  # Во время выхода из режима эта часть не выполняется, чтобы избежать продолжения без остановки
				self.MAZE_CNT = self.MAZE_CNT + 1
				print(self.MAZE_CNT)
				go.stop()
				time.sleep(0.05)
				go.back()  # Немного отступить назад
				time.sleep(0.15)
				go.stop()
				time.sleep(0.05)
				if self.MAZE_CNT > 3:  # Проверить несколько раз, есть ли препятствие, чтобы избежать ложного срабатывания
					self.MAZE_CNT = 0
					self.MAZE_ABLE = 1  # Если путь заблокирован

		else:
			go.stop()
			self.s_L = 0
			self.s_R = 0
			time.sleep(0.1)
			servo.set(7, 5)  # Сначала поверните сервопривод ультразвукового датчика направо
			if cfg.CRUISING_FLAG:
				time.sleep(0.25)
			self.s_R = self.get_distance()
			if cfg.CRUISING_FLAG:
				time.sleep(0.2)

			servo.set(7, 175)  # Затем поверните сервопривод ультразвукового датчика налево
			if cfg.CRUISING_FLAG:
				time.sleep(0.3)
			self.s_L = self.get_distance()
			if cfg.CRUISING_FLAG:
				time.sleep(0.2)
			servo.set(7, 80)  # Затем снова поверните сервопривод ультразвукового датчика в середину
			time.sleep(0.1)

			if (self.s_R == 0) or (
					self.s_R > self.s_L and self.s_R > 20):  # Если пространство справа широкое и препятствие находится далеко, и справа шире, чем слева
				self.MAZE_ABLE = 0
				cfg.LEFT_SPEED = 99  # Скорость поворота, если на разных поверхностях необходимо вручную отрегулировать скорость для достаточной силы поворота, здесь скорость для коврика должна быть выше
				cfg.RIGHT_SPEED = 99
				go.right()
				if cfg.CRUISING_FLAG:
					time.sleep(
						cfg.MAZE_TURN_TIME / 1000)  # Время поворота, регулируется в зависимости от скорости поворота, обычно достаточно повернуться примерно на 90 градусов
				cfg.LEFT_SPEED = 45
				cfg.RIGHT_SPEED = 45

			elif (self.s_L == 0) or (
					self.s_R < self.s_L and self.s_L > 20):  # Если пространство слева широкое и препятствие находится далеко, и слева шире, чем справа
				self.MAZE_ABLE = 0
				cfg.LEFT_SPEED = 99  # Скорость поворота, если на разных поверхностях необходимо вручную отрегулировать скорость для достаточной силы поворота, здесь скорость для коврика должна быть выше
				cfg.RIGHT_SPEED = 99
				go.left()
				if cfg.CRUISING_FLAG:
					time.sleep(cfg.MAZE_TURN_TIME / 1000)  # Время поворота, регулируется в зависимости от скорости поворота, обычно достаточно повернуться примерно на 90 градусов
				cfg.LEFT_SPEED = 45
				cfg.RIGHT_SPEED = 45

			else: 	# Если нет пути вперед, ни слева, ни справа, то есть вы попали в тупик, вы можете только вернуться тем же путем
				self.MAZE_ABLE = 1  # Установите флаг равным 1, чтобы избежать повторного входа в тупик, просто немного отступите назад и проверьте, есть ли другие проходы, только когда любой из проходов свободен, флаг становится равным 0, и вы можете продолжать вперед
				go.back()
				if cfg.CRUISING_FLAG:
					time.sleep(0.3)

			go.stop()
			time.sleep(0.1)