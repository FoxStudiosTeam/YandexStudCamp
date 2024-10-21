# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!
"""
@version: python3.7
@Author  : xiaor
@Explain :红外
@contact :
@Time    :2020/05/09
@File    :xr_infrared.py
@Software: PyCharm
"""
import xr_gpio as gpio
import xr_config as cfg

from xr_motor import RobotDirection

go = RobotDirection()


class Infrared(object):
	def iravoid(self):
		"""
		Инфракрасное предотвращение столкновений
		"""
		if gpio.digital_read(gpio.IR_M) == 0:  # Если средний датчик обнаружил объект
			return "True"
		else:
			return "False"
			#go.stop()
		# print("Инфракрасное предотвращение столкновений")

	def irfollow(self):
		"""
		Инфракрасное следование
		"""
		cfg.LEFT_SPEED = 30
		cfg.RIGHT_SPEED = 30
		if gpio.digital_read(gpio.IRF_L) == 0 and gpio.digital_read(gpio.IRF_R) == 0 and gpio.digital_read(gpio.IR_M) == 1:
			go.stop()  # Остановка: слева и справа обнаружены препятствия или вообще ничего не обнаружено
		else:
			if gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 0:
				cfg.LEFT_SPEED = 50
				cfg.RIGHT_SPEED = 50
				go.right()  # Левая сторона датчика не обнаружила препятствие + правая сторона обнаружила препятствие
			elif gpio.digital_read(gpio.IRF_L) == 0 and gpio.digital_read(gpio.IRF_R) == 1:
				cfg.LEFT_SPEED = 50
				cfg.RIGHT_SPEED = 50
				go.left()  # Левая сторона обнаружила препятствие + правая сторона не обнаружила препятствие
			elif gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 1 or gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 1:
				cfg.LEFT_SPEED = 50
				cfg.RIGHT_SPEED = 50
				go.forward()  # Двигаться вперед: только центральный датчик обнаружил препятствие

	def avoiddrop(self):
		"""
		Инфракрасное предотвращение падения
		"""
		cfg.LEFT_SPEED = 25
		cfg.RIGHT_SPEED = 25
		if gpio.digital_read(gpio.IR_L) == 0 and gpio.digital_read(gpio.IR_R) == 0:  # Когда оба инфракрасных датчика обнаруживают поверхность земли
			cfg.AVOIDDROP_CHANGER = 1  # Установить флаг равным 1, который будет проанализирован в последовательном порту для определения направления
		else:
			if cfg.AVOIDDROP_CHANGER == 1:  # Только когда предыдущее состояние было нормальным, выполняется остановка, чтобы избежать повторного выполнения остановки без возможности дальнейшего дистанционного управления
				go.stop()
				cfg.AVOIDDROP_CHANGER = 0