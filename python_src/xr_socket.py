# coding:utf-8
# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Модуль для работы с сетевыми соединениями
# @Time    : 2020/05/09
# @File    : xr_socket.py
# @Software: PyCharm

from builtins import range, str, eval, hex, int, object, type, abs, Exception, repr, bytes, len

import os
import time
import xr_config as cfg

from subprocess import call

from xr_motor import RobotDirection
go = RobotDirection()

from xr_servo import Servo
servo = Servo()

from xr_car_light import Car_light
car_light = Car_light()

from xr_music import Beep
beep = Beep()


class Socket:
	def __init__(self):
		self.rec_flag = 0  # Флаг получения байта 0xff
		self.count = 0  # Счетчик полученных данных
		self.client = None

	def sendbuf(self, buf):
		time.sleep(0.2)
		# print('TCP_CLIENT:%s++++++++BT_CLIENT:%s' % (cfg.TCP_CLIENT, cfg.BT_CLIENT))
		if cfg.TCP_CLIENT != False:
			try:
				cfg.TCP_CLIENT.send(buf)
				time.sleep(0.005)
				print('tcp send ok!!!')
			except Exception as e:  # Ошибка отправки
				print('tcp send error:', e)  # Отобразить сообщение об ошибке

		if cfg.BT_CLIENT != False:
			try:
				cfg.BT_CLIENT.send(buf)
				time.sleep(0.005)
				print('bluetooth send ok!!!')
			except Exception as e:  # Ошибка отправки
				print('bluetooth send error:', e)  # Отобразить сообщение об ошибке

	def load_server(self, server, servername):
		"""
		Функция сервиса сокетов
		Аргументы: self как экземпляр класса, аргумент server, который нужно запустить, buf для получаемых данных, servername типа имени службы, которую нужно запустить
		"""
		while True:
			time.sleep(0.1)
			print("waitting for %s connection..." % servername, "\r")

			if servername == 'bluetooth':  # Если выбран Bluetooth
				cfg.BT_CLIENT = False  # Выключить службу Bluetooth перед запуском
				cfg.BT_CLIENT, socket_address = server.accept()  # Инициализировать сокет и создать клиента и адрес
				client = cfg.BT_CLIENT
				time.sleep(0.1)
				print(str(socket_address[0]) + " %s connected!" % servername + "\r")  # Отобразить клиента и адрес

			elif servername == 'tcp':  # Если выбран TCP
				cfg.TCP_CLIENT = False  # Выключить службу TCP перед запуском
				cfg.TCP_CLIENT, socket_address = server.accept()  # Инициализировать сокет и создать клиента и адрес
				client = cfg.TCP_CLIENT
				time.sleep(0.1)
				print(str(socket_address[0]) + " %s connected!" % servername + "\r")  # Отобразить клиента и адрес

			while True:
				try:
					data = client.recv(cfg.RECV_LEN)  # cfg.RECV_LEN - длина принимаемых данных за один раз
					# print(data)
					if len(data) < cfg.RECV_LEN:  # Если длина данных не соответствует требованиям
						# print('Длина данных %d:  % len(data))
						break
					if data[0] == 0xff and data[len(data) - 1] == 0xff:  # Если начало и конец пакета - это 0xff, что соответствует протоколу связи Xiao-R
						buf = []  # Определить список
						for i in range(1, 4):  # Получить данные из середины пакета
							buf.append(data[i])  # Добавить данные в buf
						self.communication_decode(buf)  # Выполнить декодирование данных коммуникации
				except Exception as e:  # Ошибка получения
					time.sleep(0.1)
					print('socket received error:', e)  # Отобразить сообщение об ошибке

			client.close()  # Закрыть клиент
			client = None
			go.stop()
		go.stop()
		server.close()

	def communication_decode(self, buffer):
		"""
		   Функция декодирования данных, которая анализирует данные, полученные из сокета, в соответствии с протоколом связи Xiao-R
		   Формат протокола: 0xff, 0xXX, 0xXX, 0xXX, 0xff
		   Значения:
			 0xff - Заголовок пакета
			 0xXX - Бит типа
			 0xXX - Бит контроля
			 0xXX - Данные
			 0xff - Хвост пакета
		   После фильтрации сокетом, данные буфера будут такими: [заголовок, тип, контроль, данные]
		   """
		print(buffer)
		if buffer[0] == 0x00:  # Если первый байт равен 0x00, значит пакет содержит команду управления двигателем
			if buffer[1] == 0x01:  # Если второй байт равен 0x01, значит команда на движение вперед
				if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:  # Проверка статуса ультразвукового датчика и датчика падения, чтобы убедиться, что путь впереди чист
					go.forward()  # Движение вперед

			elif buffer[1] == 0x02:
				go.back()  # Движение назад

			elif buffer[1] == 0x03:
				if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:  # Проверка статуса ультразвукового датчика и датчика падения, чтобы убедиться, что путь впереди чист
					cfg.LIGHT_STATUS = cfg.TURN_LEFT
					go.left()  # Поворот влево

			elif buffer[1] == 0x04:
				if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:  # Проверка статуса ультразвукового датчика и датчика падения, чтобы убедиться, что путь впереди чист
					cfg.LIGHT_STATUS = cfg.TURN_RIGHT
					go.right()  # Поворот вправо

			elif buffer[1] == 0x00:
				cfg.LIGHT_STATUS = cfg.STOP
				go.stop()  # Остановка

			else:
				go.stop()

		elif buffer[0] == 0x01:  # Если первый байт равен 0x01, значит пакет содержит команду управления сервоприводом
			cfg.SERVO_NUM = buffer[1]  # Получение номера сервопривода
			cfg.SERVO_ANGLE = buffer[2]  # Получение угла сервопривода
			if abs(cfg.SERVO_ANGLE - cfg.SERVO_ANGLE_LAST) > 2:  # Предотвращение повторной отправки одного и того же угла
				cfg.ANGLE[cfg.SERVO_NUM - 1] = cfg.SERVO_ANGLE
				servo.set(cfg.SERVO_NUM, cfg.SERVO_ANGLE)

		elif buffer[0] == 0x02:  # Если первый байт равен 0x02, значит пакет содержит команду настройки скорости мотора
			if buffer[1] == 0x01:  # Если второй байт равен 0x01, значит команда на настройку скорости левого мотора
				cfg.LEFT_SPEED = buffer[2]
				go.set_speed(1, cfg.LEFT_SPEED)  # Установка скорости левого мотора
				go.save_speed()

			elif buffer[1] == 0x02:  # Если второй байт равен 0x02, значит команда на настройку скорости правого мотора
				cfg.RIGHT_SPEED = buffer[2]
				go.set_speed(2, cfg.RIGHT_SPEED)  # Установка скорости правого мотора
				go.save_speed()

		elif buffer[0] == 0x06:  # Если первый байт равен 0x06, значит пакет содержит команду установки цвета для функции отслеживания цвета
			if buffer[1] == 0x01:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['red']  # Установить цветовой диапазон на красный
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8,cfg.COLOR['red'])  # Установить свет автомобиля на красный, для уведомления

			elif buffer[1] == 0x02:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['green']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['green'])
			elif buffer[1] == 0x03:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['blue']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['blue'])
			elif buffer[1] == 0x04:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['violet']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['violet'])
			elif buffer[1] == 0x05:
				cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['orange']
				car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['orange'])
			time.sleep(1)


		elif buffer[0] == 0x13:
			if buffer[1] == 0x01 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранить текущую скорость
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['irfollow']  # Перейти в режим инфракрасного следования


			elif buffer[1] == 0x02 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  # Перейти в режим инфракрасного отслеживания линии
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранить текущую скорость
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['trackline']

			elif buffer[1] == 0x03 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  # Перейти в режим предотвращения падения
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранить текущую скорость
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['avoiddrop']


			elif buffer[1] == 0x04 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  # Перейти в режим избегания препятствий
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранить текущую скорость
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['avoidbyragar']

			elif buffer[1] == 0x05 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  # Перейти в режим отображения расстояния с помощью ультразвука
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['send_distance']

			elif buffer[1] == 0x06 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  # Перейти в режим прохождения лабиринта с помощью ультразвука
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранить текущую скорость
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				servo.set(1, 165)
				servo.set(2, 15)
				servo.set(3, 90)
				servo.set(4, 90)
				servo.set(7, 90)
				servo.set(8, 0)
				cfg.MAZE_TURN_TIME = buffer[2] * 10
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['maze']

			elif buffer[1] == 0x07:
				cfg.PROGRAM_ABLE = True
				servo.set(1, 165)
				servo.set(2, 15)
				servo.set(3, 90)
				servo.set(4, 90)
				servo.set(7, 90)
				servo.set(8, 0)

				if buffer[2] == 0x00:  # Режим видеотрансляции для проверки камеры
					go.stop()  # Остановиться
					cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # Восстановить сохраненную скорость
					cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
					cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['camera_normal']
					cfg.CRUISING_FLAG = cfg.CRUISING_SET['camera_normal']
					car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])  # Выключить свет автомобиля при выходе из режима следования за цветом

				elif buffer[2] == 0x01:  # Режим видеонаблюдения
					cfg.PROGRAM_ABLE = False
					cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранить текущую скорость
					cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
					cfg.CRUISING_FLAG = cfg.CRUISING_SET['camera_linepatrol']
					cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['camera_linepatrol']
					# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # Команда завершения видеопотока камеры
					# call("%s" % path_sh, shell=True)  # Запуск команды оболочки для завершения видеопотока камеры
					time.sleep(2)

			elif buffer[1] == 0x08:  # Режим следования за лицом
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['facefollow']
				cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['facefollow']
				# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # Команда завершения видеопотока камеры
				# call("%s" % path_sh, shell=True)  # Запуск команды оболочки для завершения видеопотока камеры
				time.sleep(2)
			elif buffer[1] == 0x09:  # Режим следования за цветом
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['colorfollow']
				cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['colorfollow']
				# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # Команда завершения видеопотока камеры
				# call("%s" % path_sh, shell=True)  # Запуск команды оболочки для завершения видеопотока камеры
				time.sleep(2)
			elif buffer[1] == 0x0A:  # Режим распознавания QR-кодов
				cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранить текущую скорость
				cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['qrcode_detection']
				cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['qrcode_detection']
				# path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # Команда завершения видеопотока камеры
				# call("%s" % path_sh, shell=True)  # Запуск команды оболочки для завершения видеопотока камеры
				time.sleep(2)
			elif buffer[1] == 0x0B:  # Световое шоу
				car_light.init_led()  # Световое шоу на автомобильных фарах
			elif buffer[1] == 0x00:  # Нормальный режим
				cfg.PROGRAM_ABLE = True
				cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # Восстановить сохраненную скорость
				cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
				cfg.AVOIDDROP_CHANGER = 1
				cfg.AVOID_CHANGER = 1
				cfg.CRUISING_FLAG = cfg.CRUISING_SET['normal']
				print("CRUISING_FLAG normal mode %d " % cfg.CRUISING_FLAG)

		elif buffer == [0x31, 0x00, 0x00]:  # Запрос информации об уровне заряда
			buf = bytes([0xff, 0x31, 0x01, cfg.POWER, 0xff])
			self.sendbuf(buf)

		elif buffer[0] == 0x32:  # Сохранение угла
			servo.store()

		elif buffer[0] == 0x33:  # Чтение угла
			servo.restore()

		elif buffer[0] == 0x40:  # Включение/выключение режима освещения
			if buffer[1] == 0x00:
				car_light.open_light()  # Включить все фары, белый свет
				cfg.LIGHT_OPEN_STATUS = 1
			elif buffer[1] == 0x01:
				car_light.close_light()  # Выключить все фары, черный цвет
				cfg.LIGHT_OPEN_STATUS = 0
			else:
				lednum = buffer[1]  # Получить количество светодиодов
				ledcolor = buffer[2]  # Получить цвет светодиода
				if lednum < 10:  # Режим многолампы
					car_light.set_ledgroup(cfg.CAR_LIGHT, lednum - 1, ledcolor)
				elif 9 < lednum < 18:  # Одноламповый режим
					car_light.set_led(cfg.CAR_LIGHT, lednum - 9, ledcolor)

		elif buffer[0] == 0x41:
			if buffer[1] == 0x00:
				tune = buffer[2]
				cfg.TUNE = tune
			# beep.tone(beep.tone_all)
			elif buffer[1] == 0x01:  # Принимаемый низкий тон
				beet1 = buffer[2]
				beep.tone(beep.tone_all[cfg.TUNE][beet1 + 14], 0.5)
			elif buffer[1] == 0x02:  # Принимаемый средний тон
				beet2 = buffer[2]
				beep.tone(beep.tone_all[cfg.TUNE][beet2], 0.5)
			elif buffer[1] == 0x03:  # Принимаемый высокий тон
				beet3 = buffer[2]
				beep.tone(beep.tone_all[cfg.TUNE][beet3 + 7], 0.5)

		elif buffer == [0xef, 0xef, 0xee]:
			print("Heartbeat Packet!")
		elif buffer[0] == 0xfc:  # Завершение работы
			os.system("sudo shutdown -h now")
		else:
			print("error command!")
	def bluetooth_server(self):
		"""
		Запуск сервиса приема Bluetooth
		Аргументы: первый аргумент указывает на сервис, который нужно запустить, второй аргумент указывает на имя службы
		"""
		# print("Загрузка bluetooth_server")
		self.load_server(cfg.BT_SERVER, 'bluetooth')
	def tcp_server(self):
		"""
		Запуск сервиса приема TCP
		Аргументы: первый аргумент указывает на сервис, который нужно запустить, второй аргумент указывает на имя службы
		"""
		# print("Загрузка tcp_server")
		self.load_server(cfg.TCP_SERVER, 'tcp')
