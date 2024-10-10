# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Упаковка конфигурационного файла
# @contact :
# @Time    : 2020/05/09
# @File    : xr_configparser.py
# @Software: PyCharm

from configparser import ConfigParser


class HandleConfig:
    """
    Пакет для чтения и записи данных конфигурации
    """
    def __init__(self, filename):
        """
        :param filename: имя файла конфигурации
        """
        self.filename = filename
        self.config = ConfigParser()  # Создание парсера конфигурации для чтения файла
        self.config.read(self.filename, encoding="utf-8")  # Чтение конфигурационного файла

    def save_data(self, group, key, data):
        if not self.config.has_section(group):  # Проверка наличия секции
            self.config.add_section(group)  # Добавить секцию, если она отсутствует
        self.config.set(group, key, str(data))  # Запись данных в секцию
        with open(self.filename, "w") as file:  # Сохранение в файл
            self.config.write(file)

    def get_data(self, group, key):
        data = self.get_value(group, key)  # Чтение данных
        data = str(data)[1:-1].split(',')
        data = list(map(int, data))
        return data

    def get_value(self, section, option):
        return self.config.get(section, option)