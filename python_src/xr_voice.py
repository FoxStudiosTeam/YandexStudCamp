# # coding: utf-8
# """
# Wi-Fi видеоробот-тележка на Raspberry Pi
# Автор: Sence
# Все права защищены: Xiao-R Technology (глубокая компания Shenzhen Xiaoer Geek Technology Co., Ltd.) ; WIFI робот форум www.wifi-robots.com
# Этот код может быть свободно изменен, но запрещено использовать его в коммерческих целях!
# Этот код уже подан на получение авторских прав на программное обеспечение, поэтому немедленно подавайте иск, если обнаружите нарушение!
# """
# """
# @version: python3.7
# @Автор : xiaor
# @Объяснение : Модуль голоса
# @Дата : 2020/05/09
# @Файл : xr_voice.py
# @Программное обеспечение: PyCharm
# """
import serial
import time
import xr_config as cfg


class Voice(object):
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyS0", 9600)
        pass

    def run(self):
        while True:
            while self.ser.inWaiting() > 0:
                time.sleep(0.05)
                n = self.ser.inWaiting()
                myout = self.ser.read(n)
                self.get_voice(myout)
                dat = int.from_bytes(myout, byteorder='big')
                print('%#x' % dat)

            time.sleep(0.5)

    def get_voice(self, data):
        cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        if len(data) < cfg.RECV_LEN:  # Если длина данных меньше ожидаемого значения
            # print('data len %d:'%len(data))
            return cfg.VOICE_MOD
        if data[0] == 0xff and data[len(data) - 1] == 0xff:  # Если начало и конец пакета равны 0xff
            buf = []  # Определить список
            for i in range(1, 4):  # Получить данные из середины пакета
                buf.append(data[i])  # Добавить данные в buf
            if buf[0] == 0xf5 and buf[1] == 0x01:
                if buf[2] == 0x01:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
                elif buf[2] == 0x02:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['openlight']
                elif buf[2] == 0x03:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['closelight']
                elif buf[2] == 0x06:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['forward']
                elif buf[2] == 0x07:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['back']
                elif buf[2] == 0x08:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['left']
                elif buf[2] == 0x09:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['right']
                elif buf[2] == 0x0A:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['stop']
                elif buf[2] == 0x0B:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['nodhead']
                elif buf[2] == 0x0C:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['shakehead']
            return cfg.VOICE_MOD

if __name__ == "__main__":
    ser = Voice()
    while True:
        print("run voice ctl")
        ser.run()