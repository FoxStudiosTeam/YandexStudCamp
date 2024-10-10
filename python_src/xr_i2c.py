# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# Форум WiFi Robot: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!
"""
@version: python3.7
@Author  : xiaor
@Explain :i2c
@contact :
@Time    :2020/05/09
@File    :xr_i2c.py
@Software: PyCharm
"""
import os
import time
from builtins import IOError, object, len

import smbus


# # smbus
# self.device = smbus.SMBus(1)  # 0 представляет /dev/i2c0 1 представляет /dev/i2c1
# # I2C адрес устройства
# address = 0x18


class I2c(object):
    def __init__(self):
        self.mcu_address = 0x18
        self.ps2_address = 0x19
        self.device = smbus.SMBus(1)
        pass

    def writedata(self, address, values):
        """
        # Запись данных в I2C адрес
        """
        try:
            self.device.write_i2c_block_data(address, values[0],
                                             values[1:len(values)])  # последовательная запись, первый параметр: адрес устройства, второй параметр: регистр записи, третий параметр: данные для записи
            time.sleep(0.005)
        except Exception as e:  # ошибка записи
            pass
            # print('ошибка i2c записи:', e)
            # os.system('sudo i2cdetect -y 1')

    def readdata(self, address, index):
        """
        # Чтение одного байта данных из I2C
        """
        try:
            value = self.device.read_byte_data(address, index)  # чтение одного байта данных с регистра устройства с индексом index
            time.sleep(0.005)
            return value  # возвращает прочитанные данные
        except Exception as e:  # ошибка чтения
            pass
            # print('ошибка i2c чтения:', e)
            # os.system('sudo i2cdetect -y 1')
