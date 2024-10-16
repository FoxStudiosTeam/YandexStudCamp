# coding:utf-8
"""
Wi-Fi видеоробот-тележка на Raspberry Pi
Автор: Sence
Все права защищены: Xiao-R Technology (глубокая компания Shenzhen Xiaoer Geek Technology Co., Ltd.) ; WIFI робот форум www.wifi-robots.com
Этот код можно свободно изменять, но запрещено использовать его в коммерческих целях!
Этот код уже подан на получение авторских прав на программное обеспечение, поэтому немедленно подавайте иск, если обнаружите нарушение!
"""
"""
@version: python3.7
@Автор : xiaor
@Объяснение : OLED дисплей
@контакт :
@Дата : 2020/05/09
@Файл : xr_oled.py
@Программное обеспечение: PyCharm
"""
import time
import os
import subprocess
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from xr_ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()

import xr_config as cfg


class Oled():
	def __init__(self):
		# Получаем экземпляр OLED
		self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)
		# Инициализация, очистка экрана
		self.disp.begin()
		self.disp.clear()
		self.disp.display()

		# Создаем новое изображение размером с размер OLED
		self.width = self.disp.width
		self.height = self.disp.height
		self.image = Image.new('1', (self.width, self.height))

		# Загружаем изображение в объект рисования, аналогично загрузке на холст
		self.draw = ImageDraw.Draw(self.image)

		# Рисуем черную заливку, чтобы очистить изображение
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		# Draw a black filled box to clear the image.
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		# Draw some shapes.
		# Сначала определяем некоторые константы, чтобы упростить изменение формы фигур.
		self.padding = -2
		self.top = self.padding
		self.bottom = self.height - self.padding
		# Перемещаемся слева направо, отслеживая текущую позицию x для рисования фигур.

		# Выбор шрифта
		# Шрифты по умолчанию в библиотеке, находятся в ImageFont
		self.font = ImageFont.load_default()
		# Библиотека шрифтов на Raspberry Pi, позволяет задавать размер шрифта
		self.font1 = ImageFont.truetype('/home/pi/work/python_src/simhei.ttf', 14)
		pass

	def cpu_temp(self):
		'''
		   # Получение температуры процессора Raspberry Pi
		   '''
		# Температура CPU хранится в этом файле, откройте файл
		tempFile = open('/sys/class/thermal/thermal_zone0/temp')
		# Прочитайте файл
		cputemp = tempFile.read()
		# Закройте файл
		tempFile.close()
		# Округление до ближайшего целого числа
		tem = round(float(cputemp) / 1000, 1)
		return str(tem)

	def get_network_interface_state(self, interface):
		'''
		   Получение состояния подключения сетевого интерфейса. Возвращает up, если подключено, иначе возвращает down.
		   '''
		return subprocess.check_output('cat /sys/class/net/%s/operstate' % interface, shell=True).decode('ascii')[
			   :-1]

	def get_ip_address(self, interface):
		'''
		   Получение IP-адреса сети
		   '''
		if self.get_network_interface_state(interface) == 'down':  # Проверка состояния подключения
			return None
		cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface  # Поиск IP-адреса для соответствующего сетевого интерфейса
		return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]

	def get_ip_address_wlan(self, interface):
		'''
		   Получение IP-адреса сети
		   '''
		if self.get_network_interface_state(interface) == 'down':  # Проверка состояния подключения
			return None
		cmd = "ip a show dev %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | grep -v '169'" % interface  # Поиск IP-адреса для соответствующего сетевого интерфейса
		return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]

	def draw_row_column(self, row, column, strs):
		'''
		Строчное отображение, row представляет номер строки, column представляет номер столбца, strs представляет строку, которую нужно отобразить.
		'''
		if row == 1:
			self.draw.text((column, self.top), strs, font=self.font, fill=255)
		elif row == 2:
			self.draw.text((column, self.top + 8), strs, font=self.font, fill=255)
		elif row == 3:
			self.draw.text((column, self.top + 16), strs, font=self.font, fill=255)
		elif row == 4:
			self.draw.text((column, self.top + 25), strs, font=self.font, fill=255)

	def disp_default(self):
		'''
		Информация, отображаемая при запуске, включая ip-адрес проводной сети, ip-адрес беспроводной сети, использование памяти и использование SD-карты.
		'''
		# Рисуем черную заливку, чтобы очистить изображение.
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		# Скрипты оболочки для мониторинга системы отсюда: https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
		cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell=True)
		cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.1f%%\", $3,$2,$3*100/$2 }'"
		MemUsage = subprocess.check_output(cmd, shell=True)
		cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
		Disk = subprocess.check_output(cmd, shell=True)

		# Пишем две строки текста.
		self.draw_row_column(1, 0, "eth0: " + str(self.get_ip_address('eth0')))
		self.draw_row_column(2, 0, "wlan0: " + str(self.get_ip_address('wlan0')))
		self.draw_row_column(3, 0, str(MemUsage.decode('utf-8')))
		self.draw_row_column(4, 0, str(Disk.decode('utf-8')))

		# Отображение изображения.

		self.disp.image(self.image)
		self.disp.display()
		time.sleep(0.1)

	def disp_cruising_mode(self):
		'''
		Режим отображения после входа в режим управления
		:return: none
		'''
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

		dispmod = cfg.OLED_DISP_MOD[cfg.CRUISING_FLAG]  # Отображение режима в соответствии с выбранным режимом
		dispmodlength = len(dispmod) * cfg.OLED_DISP_MOD_SIZE  # Получение длины строки
		positionmod = (128 - dispmodlength) / 2 - 1  # Начальная позиция символов

		self.draw.text((0, -2), subprocess.check_output('iwgetid -r', shell=True), font=self.font, fill=255)  # Отображение логотипа (Теперь название сети)
		for line in os.popen(
				"ifconfig wlan0 | awk  '/ether/{print $2 ;exit}' |sed 's/\://g'"):  # Получение MAC-адреса wlan0
			mac = (line[6:12])  # Получение последних 6 символов MAC-адреса
			mac = 'id:' + mac
		self.draw.text((74, 8), mac, font=self.font, fill=255)  # Отображение последних 4 символов MAC-адреса
		self.draw.text((0, 8), "Dis:" + str(cfg.DISTANCE) + "cm", font=self.font,
					   fill=255)  # Отображение расстояния
		# self.draw.text((positionmod, 17), dispmod, font=self.font1, fill=255)  # Отображение режима

		self.draw.line((0, 8, 128, 8), fill=255)  # Горизонтальная линия

		# Рисование рамки батареи
		m = 3  # Количество уровней заряда батареи
		n = 3  # Количество пикселей, занимаемых каждым уровнем
		batlength = m * n + 2 + 2 + 2  # m*n обозначает количество пикселей, занятых ядром, первый 2 - расстояние между ядром и краями, второй 2 - ширина рамок вокруг ядра, третий 2 - ширина верхнего и нижнего углов
		x = 128 - batlength - 1  # Начальное положение батарейного фрейма слева
		y = 0  # Начальное положение батарейного фрейма сверху

		# Рисование рамки батареи
		self.draw.line((x, y + 2, x + 2, y + 2), fill=255)
		self.draw.line((x + 2, y + 2, x + 2, y), fill=255)
		self.draw.line((x + 2, y, x + batlength, y), fill=255)
		self.draw.line((x + batlength, y, x + batlength, y + 5), fill=255)
		self.draw.line((x + batlength, y + 5, x + 2, y + 5), fill=255)
		self.draw.line((x + 2, y + 5, x + 2, y + 3), fill=255)
		self.draw.line((x + 2, y + 3, x, y + 3), fill=255)
		self.draw.line((x, y + 3, x, y + 2), fill=255)
		# Расчет уровня заряда
		level = cfg.POWER
		# Очистка уровня заряда
		self.draw.line((x + 3, y + 2, x + batlength - 2, y + 2), fill=0)
		self.draw.line((x + 3, y + 3, x + batlength - 2, y + 3), fill=0)
		# Обновление уровня заряда
		self.draw.line((x + batlength - 2 - level * n, y + 2, x + batlength - 2, y + 2), fill=255)
		self.draw.line((x + batlength - 2 - level * n, y + 3, x + batlength - 2, y + 3), fill=255)
		# Отображение информации на экране OLED
		ip_address = self.get_ip_address_wlan('wlan0').split("\n")
		# print(ip_address)
		for idx, ip in enumerate(ip_address):
			self.draw_row_column(idx + 3, 0, "wlan:" + str(ip))
		self.disp.image(self.image)
		self.disp.display()
		time.sleep(0.05)
