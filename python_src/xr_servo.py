# coding:utf-8
# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Управление сервоприводами
# @contact :
# @Time    : 2020/05/09
# @File    : XiaoR_servo.py
# @Software: PyCharm

from builtins import hex, eval, int, object
from xr_i2c import I2c
import os

i2c = I2c()
import xr_config as cfg

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)


class Servo(object):
    """
    Класс управления сервоприводами
    """
    def __init__(self):
        pass

    def angle_limit(self, angle):
        """
        Ограничивает угол сервопривода, чтобы предотвратить блокировку и повреждение
        """
        if angle > cfg.ANGLE_MAX:  # Ограничение максимального угла
            angle = cfg.ANGLE_MAX
        elif angle < cfg.ANGLE_MIN:  # Ограничение минимального угла
            angle = cfg.ANGLE_MIN
        return angle

    def set(self, servonum, servoangle):
        """
        Устанавливает угол сервопривода
        :param servonum: Номер сервопривода
        :param servoangle: Угол сервопривода
        :return:
        """
        angle = self.angle_limit(servoangle)
        buf = [0xff, 0x01, servonum, angle, 0xff]
        try:
            i2c.writedata(i2c.mcu_address, buf)
        except Exception as e:
            print('Ошибка при записи сервопривода:', e)

    def store(self):
        """
        Сохраняет углы сервоприводов
        :return:
        """
        cfgparser.save_data("servo", "angle", cfg.ANGLE)

    def restore(self):
        """
        Восстанавливает углы сервоприводов
        :return:
        """
        cfg.ANGLE = cfgparser.get_data("servo", "angle")
        for i in range(0, 8):
            cfg.SERVO_NUM = i + 1
            cfg.SERVO_ANGLE = cfg.ANGLE[i]
            self.set(i + 1, cfg.ANGLE[i])
