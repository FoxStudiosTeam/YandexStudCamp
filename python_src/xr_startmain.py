# coding:utf-8
# Код для управления WiFi-роботом на базе Raspberry Pi с использованием беспроводного видео
# Автор: Sence
# Все права защищены: XiaoR Technology (глубоко интегрированная компания Shenzhen XiaoEr Geek Technology Co., Ltd.; www.xiao-r.com) и форум WIFI-роботов www.wifi-robots.com
# Этот код может быть свободно изменен, но запрещено использовать его в коммерческих целях!
# На этот код подана заявка на защиту авторских прав программного обеспечения, и любые нарушения будут немедленно преследоваться по закону!
import sys

from fs_custom_light import CustomLight

# @version: python3.7
# @Author  : xiaor
# @Explain : главный поток
# @Time    : 2020/05/09
# @File    : xr_startmain.py
# @Software: PyCharm

import os
import time
import threading
from threading import Timer
from subprocess import call

import fs_event as fs_ev
from fs_motor import FSMover
import xr_config as cfg
from fs_move_hand import Hand
from fs_movement import FsMovement
from fs_neuro_thread import NeuroThread
from xr_motor import RobotDirection

go = RobotDirection()
from xr_socket import Socket

socket = Socket()
from xr_infrared import Infrared

infrared = Infrared()
from xr_ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()
from xr_camera import Camera

camera = Camera()
from xr_function import Function

function = Function()
from xr_oled import Oled

try:
    oled = Oled()
except:
    print('oled initialization fail')
from xr_music import Beep

beep = Beep()
from xr_power import Power

power = Power()
from xr_servo import Servo

servo = Servo()
from xr_ps2 import PS2

ps2 = PS2()
from xr_i2c import I2c

i2c = I2c()
from xr_voice import Voice

voice = Voice()




def cruising_mode():
    # Функция для переключения режимов
    # :return: none
    # print('pre_CRUISING_FLAG：{}'.format(cfg.PRE_CRUISING_FLAG))
    time.sleep(0.001)
    if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_FLAG:  # Если режим цикла изменился
        cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # При смене режима восстановить сохраненную скорость
        cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
        if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_SET[
            'normal']:  # Если режим цикла изменился, и предыдущий режим не был нормальным
            go.stop()  # Сначала остановить машину
        cfg.PRE_CRUISING_FLAG = cfg.CRUISING_FLAG  # Обновить значение флага предыдущего режима

    if cfg.CRUISING_FLAG == cfg.CRUISING_SET['irfollow']:  # Переход в режим следования за инфракрасным лучом
        # print("Infrared.irfollow")
        infrared.irfollow()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['trackline']:  # Переход в режим отслеживания линии по инфракрасному лучу
        # print("Infrared.trackline")
        infrared.trackline()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET[
        'avoiddrop']:  # Переход в режим предотвращения падения с помощью инфракрасного луча
        # print("Infrared.avoiddrop")
        infrared.avoiddrop()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET[
        'avoidbyragar']:  # Переход в режим предотвращения столкновений с помощью ультразвукового датчика
        # print("Ultrasonic.avoidbyragar")
        ultrasonic.avoidbyragar()
        time.sleep(0.5)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET[
        'send_distance']:  # Переход в режим измерения расстояния с помощью ультразвукового датчика
        # print("Ultrasonic.send_distance")
        ultrasonic.send_distance()
        time.sleep(1)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET[
        'maze']:  # Переход в режим прохождения лабиринта с помощью ультразвукового датчика
        # print("Ultrasonic.maze")
        ultrasonic.maze()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['camera_normal']:  # Переход в режим отладки
        time.sleep(2)
        print("CRUISING_FLAG == 7")
        # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'
        # call("%s" % path_sh, shell=True)
        cfg.CRUISING_FLAG = cfg.CRUISING_SET['normal']

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET[
        'camera_linepatrol']:  # Переход в режим управления камерой для отслеживания линий
        function.linepatrol_control()
        time.sleep(0.01)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET[
        'qrcode_detection']:  # Переход в режим распознавания и идентификации QR-кодов
        function.qrcode_control()
        time.sleep(0.01)
    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:

        if cfg.VOICE_MOD == cfg.VOICE_MOD_SET['normal']:
            time.sleep(0.001)
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['openlight']:  # Включить свет
            # car_light.open_light()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['closelight']:  # Выключить свет
            # car_light.close_light()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['forward']:  # Двигаться вперед
            go.forward()
            time.sleep(2)
            go.stop()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['back']:  # Двигаться назад
            go.back()
            time.sleep(2)
            go.stop()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['left']:  # Повернуть влево
            cfg.LIGHT_STATUS = cfg.TURN_LEFT
            go.left()
            time.sleep(0.8)
            go.stop()
            cfg.LIGHT_STATUS = cfg.STOP
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['right']:  # Повернуть вправо
            cfg.LIGHT_STATUS = cfg.TURN_RIGHT
            go.right()
            time.sleep(0.8)
            go.stop()
            cfg.LIGHT_STATUS = cfg.STOP
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['stop']:  # Остановиться
            go.stop()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['nodhead']:  # Пожалуйста, кивните головой
            for i in range(1, 4):
                if i:
                    for j in range(90, 0, -5):
                        print(j)
                        servo.set(8, j)
                        time.sleep(0.04)
                    time.sleep(0.1)
            servo.set(8, 0)
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['shakehead']:  # Пожалуйста, покачайте головой
            for i in range(1, 3):
                if i:
                    for j in range(45, 135, 5):
                        # print(j)
                        servo.set(7, j)
                        time.sleep(0.02)
                    time.sleep(0.1)
                    for j in range(135, 45, -5):
                        # print(j)
                        servo.set(7, j)
                        time.sleep(0.02)
                    time.sleep(0.1)
            servo.set(7, 90)
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']

    else:
        time.sleep(0.001)


def status():
    """
    Функция обновления статуса, включая обновление функций, таких как фары автомобиля и OLED, которые требуют периодического обновления.
    :return:
    """
    if cfg.PROGRAM_ABLE:  # Если система находится в состоянии работы
        if cfg.LOOPS > 30:  # Обновление функции происходит каждые 0.1 секунды, здесь это равно проверке направления машины через каждые 0.3 секунды и включению соответствующих сигнальных огней в зависимости от направления движения
            if cfg.LIGHT_STATUS == cfg.TURN_FORWARD:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS  # Перед входом в управление направлением, присваиваем текущее состояние статусу последнего состояния
            # car_light.forward_turn_light()
            elif cfg.LIGHT_STATUS == cfg.TURN_BACK:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
            # car_light.back_turn_light()
            elif cfg.LIGHT_STATUS == cfg.TURN_LEFT:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
            # car_light.left_turn_light()
            elif cfg.LIGHT_STATUS == cfg.TURN_RIGHT:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
            # car_light.right_turn_light()
            # elif cfg.LIGHT_STATUS == cfg.STOP and cfg.LIGHT_LAST_STATUS != cfg.LIGHT_STATUS:  # Зажигание лампы STOP выполняется только один раз при длительной остановке
            # 	cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
            # 	if cfg.LIGHT_OPEN_STATUS == 1:
            # 		#car_light.open_light()
            # 	else:
            # 		#car_light.close_light()
        if cfg.LOOPS > 100:  # Таймер установлен на 0.01 секунды входа, превышение 100 указывает на то, что произошло 100 изменений, что составляет одну секунду времени. Некоторые данные, которые не нужно обновлять слишком часто, могут быть размещены здесь
            cfg.LOOPS = 0  # Очистка LOOPS
            # power.show_vol()  # Показание индикатора заряда батареи
            try:
                oled.disp_cruising_mode()  # отображение режима OLED
            except:
                print('failed to initialized OLED')

    loops = cfg.LOOPS  # Использование промежуточной переменной для увеличения значения
    loops = loops + 1
    cfg.LOOPS = loops  # Установка значения обратно

    loops = cfg.PS2_LOOPS  # Использование промежуточной переменной для увеличения значения
    loops = loops + 1
    cfg.PS2_LOOPS = loops  # Установка значения обратно

    Timer(0.01, status).start()  # Каждый вход требует повторного запуска таймера


if __name__ == '__main__':
    '''
    Основной вход программы
    '''
    print("....wifirobots start!...")

    os.system("sudo hciconfig hci0 name XiaoRGEEK")  # Устанавливаем имя Bluetooth
    time.sleep(0.1)
    os.system("sudo hciconfig hci0 reset")  # Перезагружаем Bluetooth
    time.sleep(0.3)
    os.system("sudo hciconfig hci0 piscan")  # Восстанавливаем возможность сканирования Bluetooth
    time.sleep(0.2)
    print("now bluetooth discoverable")

    # servo.restore()  # Возвращаем положение серводвигателя к исходному
    try:
        oled.disp_default()  # Отображаем начальную информацию на OLED
    except:
        print('Не удалось инициализировать OLED.')
# car_light.init_led()  # Инициализируем светодиоды автомобиля

fs_custom_light = CustomLight()
time.sleep(0.1)
fs_motor = FSMover()

fs_neuro_thread = NeuroThread(fs_motor)

# Список потоков
threads = []

# Поток для сбора данных камеры и их обработки
t1 = threading.Thread(target=camera.run, args=())
threads.append(t1)

# Создание нового Bluetooth-потока
t2 = threading.Thread(target=socket.bluetooth_server, args=())
threads.append(t2)

# Создание нового TCP-потока через WiFi
t3 = threading.Thread(target=socket.tcp_server, args=())
threads.append(t3)

# Поток для голосового модуля
t4 = threading.Thread(target=voice.run, args=())
threads.append(t4)

# Поток для работы с пользовательским освещением
t5 = threading.Thread(target=fs_custom_light.run, args=())
threads.append(t5)

#Поток для работы с нейронной сетью
t_neural = threading.Thread(target=fs_neuro_thread.run, args=())
threads.append(t_neural)

# Создаем таймер
ti = threading.Timer(0.1, status)
ti.start()

# Команда для запуска start_mjpg_streamer
#path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'

path_sh = 'sh /home/pi/work/mjpg-streamer-master/mjpg-streamer-experimental/start.sh'
call("%s" % path_sh, shell=True)
time.sleep(1)

# Цикл по всем потокам
for t in threads:
    # print("theads %s ready to start..." % t)
    t.setDaemon(True)  # Установить поток как фоновый
    t.start()  # Запустить поток
    time.sleep(0.05)
# print("theads %s start..." %t)
print("all theads start...>>>>>>>>>>>>")
# Восстановить сохраненный угол сервопривода
servo.restore()

# Восстановить сохраненную скорость двигателя
go.motor_init()
# Основной цикл программы

fs_movement = FsMovement()

# fs_ev.bus.emit('first_move', fs_movement, fs_motor)

Hand().normal_state()

fs_ev.bus.emit('1sec_test', fs_movement, fs_motor)

while True:
    '''
    Главный цикл программы
    '''
    try:
        if cfg.PROGRAM_ABLE:  # Если системный флаг программы включен
            cfg.PS2_LOOPS = cfg.PS2_LOOPS + 1
            if cfg.PS2_LOOPS > 20:
                ps2.control()
                cfg.PS2_LOOPS = 0
    except Exception as e:  # Ловить и печатать ошибку
        time.sleep(0.1)
        print('Ошибка cruising_mod:', e)
