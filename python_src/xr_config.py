# coding:utf-8
"""
Этот скрипт является драйвером для Wi-Fi робота, который использует
Python версии 3.7. Автор: xiaor.

Этот код может быть свободно модифицирован, однако он запрещен к использованию
в коммерческих целях! Данный код защищен авторским правом и любое нарушение
может привести к судебному преследованию.

Этот код был подан на регистрацию программного обеспечения и любые нарушения
прав будут немедленно преследоваться в суде.
"""

"""
@version: python3.7
@Author  : xiaor
@Explain : конфигурация
@contact :
@Time    :2020/05/09
@File    :xr_config.py
@Software: PyCharm
"""

from socket import *
import numpy as np


# Текущий режим движения
CRUISING_FLAG = 0
# Режим предварительного движения
PRE_CRUISING_FLAG = 0
# Набор режимов движения
CRUISING_SET = {'normal': 0, 'irfollow': 1, 'trackline': 2, 'avoiddrop': 3, 'avoidbyragar': 4, 'send_distance': 5,
                 'maze': 6, 'camera_normal': 7, 'camera_linepatrol': 8, 'facefollow':9, 'colorfollow':10, 'qrcode_detection':11}
# Набор режимов камеры
CAMERA_MOD_SET = {'camera_normal': 0, 'camera_linepatrol': 1, 'facefollow':2, 'colorfollow':3, 'qrcode_detection':4}

# Максимальное значение угла сервопривода
ANGLE_MAX = 180
# Минимальное значение угла сервопривода
ANGLE_MIN = 10

# Режим голоса
VOICE_MOD = 0
# Набор режимов голоса
VOICE_MOD_SET = {'normal': 0, 'openlight': 1, 'closelight': 2, 'forward': 3, 'back': 4, 'left': 5,
                 'right': 6, 'stop': 7, 'nodhead': 8, 'shakehead':9}

# Флаг обнаружения пути
PATH_DECT_FLAG = 0
# Скорость слева
LEFT_SPEED = 68
# Скорость справа
RIGHT_SPEED = 70
# Предыдущая скорость слева
LASRT_LEFT_SPEED = 100
# Предыдущая скорость справа
LASRT_RIGHT_SPEED = 100

# Номер сервопривода
SERVO_NUM = 1
# Текущее значение угла сервопривода
SERVO_ANGLE = 90
# Последнее значение угла сервопривода
SERVO_ANGLE_LAST = 90
# Массив углов сервоприводов
ANGLE = [90, 90, 90, 90, 90, 90, 90, 5]

# Значение расстояния
DISTANCE = 0
# Флаг изменения для избегания препятствий
AVOID_CHANGER = 1
# Флаг изменения для предотвращения падения
AVOIDDROP_CHANGER = 1

# Время поворота в лабиринте
MAZE_TURN_TIME = 400

# Режим камеры
CAMERA_MOD = 0
# Линия камеры точки 1
LINE_POINT_ONE = 320
# Линия камеры точки 2
LINE_POINT_TWO = 320

# Клоппер
CLAPPER = 4
# Скорость звучания
BEET_SPEED = 50
# Музыкальная нота
TUNE = 0

# Значение опорного напряжения
VREF = 5.12
# Значение мощности
POWER = 3
# Количество циклов
LOOPS = 0
# Количество циклов PS2
PS2_LOOPS = 0

# Состояние выполнения программы
PROGRAM_ABLE = True

# Состояние фары
LIGHT_STATUS = 0
# Предыдущее состояние фары
LIGHT_LAST_STATUS = 0
# Состояние открытия фары
LIGHT_OPEN_STATUS = 0
# Состояние остановки
STOP = 1
# Состояние движения вперед
TURN_FORWARD = 2
# Состояние движения назад
TURN_BACK = 3
# Состояние поворота влево
TURN_LEFT = 4
# Состояние поворота вправо
TURN_RIGHT = 5
# Флаг установки индикатора мощности
POWER_LIGHT = 1
# Флаг установки фары
CAR_LIGHT = 2

# Цветовая схема RGB
COLOR = {'black': 0, 'red': 1, 'orange': 2, 'yellow': 3, 'green': 4, 'Cyan': 5,
         'blue': 6, 'violet': 7, 'white': 8}

# Логотип для отображения на OLED
LOGO = "XiaoR GEEK"
# Отображаемые сообщения на OLED
OLED_DISP_MOD = ["正常模式", "红外跟随", "红外巡线", "红外防掉落", "超声波避障",
                 "超声波距离显示", "超声波走迷宫", "摄像头调试",
                 "摄像头巡线", "人脸检测跟随", "颜色检测跟随", "二维码识别",
                 ]
# Размер шрифта для отображения на OLED
OLED_DISP_MOD_SIZE = 16

# Клиент Bluetooth
BT_CLIENT = False
# Клиент TCP
TCP_CLIENT = False
# Длина принятых данных
RECV_LEN = 5

# Параметры сервера Bluetooth
BT_SERVER = socket(AF_INET, SOCK_STREAM)
BT_SERVER.bind(('', 2002))  # Связывание порта 2002 для Bluetooth
BT_SERVER.listen(1)

# Определение кнопок джойстика PS2
PS2_ABLE = False  # Флаг подключения джойстика PS2
PS2_READ_KEY = 0  # Читаемое значение клавиш PS2
PS2_LASTKEY = 0  # Предыдущее читаемое значение клавиш PS2
PS2_KEY = {'PSB_PAD_UP': 1, 'PSB_PAD_DOWN': 2, 'PSB_PAD_LEFT': 3, 'PSB_PAD_RIGHT': 4,
           'PSB_RED': 5, 'PSB_PINK': 6, 'PSB_GREEN': 7, 'PSB_BLUE': 8}  # Клавиши управления джойстиком PS2

# Цветовые диапазоны для следования
# Нижняя граница цветового диапазона
COLOR_LOWER = [
    # Красный
    np.array([0, 43, 46]),
    # Зеленый
    np.array([35, 43, 46]),
    # Синий
    np.array([100, 43, 46]),
    # Фиолетовый
    np.array([125, 43, 46]),
    # Оранжевый
    np.array([11, 43, 46])
]
# Верхняя граница цветового диапазона
COLOR_UPPER = [
    # Красный
    np.array([10, 255, 255]),
    # Зеленый
    np.array([77, 255, 255]),
    # Синий
    np.array([124, 255, 255]),
    # Фиолетовый
    np.array([155, 255, 255]),
    # Оранжевый
    np.array([25, 255, 255])
]
COLOR_FOLLOW_SET = {'красный': 0, 'зеленый': 1, 'синий': 2, 'фиолетовый': 3, 'оранжевый': 4}  # Индексы цветовых диапазонов для следования
COLOR_INDEX = 0  # Индекс цветового диапазона

# Дата сканирования штрих-кода
BARCODE_DATE = None
# Тип сканированного штрих-кода
BARCODE_TYPE = None