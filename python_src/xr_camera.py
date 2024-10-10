# coding:utf-8

# Код драйвера робота Raspberry Pi WiFi
# Автор: Sence
# Авторское право: Xiao-R Technology Co., Ltd. (Shenzhen Xiao Er Geek Tech Co., Ltd.) www.xiao-r.com
# WIFI Robot Forum: www.wifi-robots.com
# Этот код можно свободно модифицировать, но его запрещено использовать в коммерческих целях!
# На этот код подана заявка на защиту авторских прав на программное обеспечение. При обнаружении нарушения немедленно будет подан иск!

# @version: python3.7
# @Author  : xiaor
# @Explain : Функции для распознавания камеры
# @contact :
# @Time    : 2020/05/09
# @File    : xr_camera.py
# @Software: PyCharm

from builtins import range, len, int
import os
from subprocess import call
import time
import math
import pyzbar.pyzbar as pyzbar
import xr_config as cfg

from xr_motor import RobotDirection

go = RobotDirection()
import cv2

from xr_servo import Servo

servo = Servo()

from xr_pid import PID


class Camera(object):
    def __init__(self):
        self.fre_count = 1  # Количество выборок
        self.px_sum = 0  # Накопленная сумма точек X
        self.cap_open = 0  # Флаг открытия камеры
        self.cap = None

        self.servo_X = 7
        self.servo_Y = 8

        self.angle_X = 90
        self.angle_Y = 20

        self.X_pid = PID(0.03, 0.09, 0.0005)  # Инициализация PID алгоритма для оси X
        self.X_pid.setSampleTime(0.005)  # Установка периода для PID алгоритма
        self.X_pid.setPoint(240)  # Установка целевого значения для PID алгоритма, 240 – это середина экрана по X, так как ширина экрана составляет 320 пикселей

        self.Y_pid = PID(0.035, 0.08, 0.002)  # Инициализация PID алгоритма для оси Y
        self.Y_pid.setSampleTime(0.005)  # Установка периода для PID алгоритма
        self.Y_pid.setPoint(160)  # Установка целевого значения для PID алгоритма, 160 – это середина экрана по Y, так как высота экрана составляет 320 пикселей

    def linepatrol_processing(self):
        """
        Обработка данных для следования по линии
        :return:
        """
        while True:
            if self.cap_open == 0:  # Камера не открыта
                try:
                    # self.cap = cv2.VideoCapture(0)  # Открытие камеры
                    self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                except Exception as e:
                    print('opencv camera open error:', e)
                self.cap_open = 1  # Установка флага открытия камеры
            else:
                try:
                    ret, frame = self.cap.read()  # Получение кадра с камеры
                    if ret:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Преобразование из RGB в Grayscale
                        if cfg.PATH_DECT_FLAG == 0:
                            ret, thresh1 = cv2.threshold(gray, 100, 255,
                                                         cv2.THRESH_BINARY)  # Бинарное пороговое значение для черной линии
                        else:
                            ret, thresh1 = cv2.threshold(gray, 100, 255,
                                                         cv2.THRESH_BINARY_INV)  # Бинарное пороговое значение для белой линии
                        for j in range(0, 640,
                                       5):  # Горизонтальный сбор данных по X, интервал между выборками 5 пикселей
                            if thresh1[350, j] == 0:  # Проверка значения пикселя на середине высоты изображения (350)
                                self.px_sum += j  # Сумма координат X точек, соответствующих цвету линии
                                self.fre_count += 1  # Сумма собранных данных
                        cfg.LINE_POINT_ONE = self.px_sum / self.fre_count  # Среднее значение координаты X точек, соответствующих цвету линии
                        self.px_sum = 0  # Очистка накопленного значения
                        self.fre_count = 1  # Очистка количества сборок (минимальное количество равно 1)
                        for j in range(0, 640,
                                       5):  # Горизонтальный сбор данных по X, интервал между выборками 5 пикселей
                            if thresh1[200, j] == 0:  # Проверка значения пикселя на середине высоты изображения (200)
                                self.px_sum += j  # Сумма координат X точек, соответствующих цвету линии
                                self.fre_count += 1  # Сумма собранных данных
                        cfg.LINE_POINT_TWO = self.px_sum / self.fre_count  # Среднее значение координаты X точек, соответствующих цвету линии
                        self.px_sum = 0  # Очистка накопленного значения
                        self.fre_count = 1  # Очистка количества сборок (минимальное количество равно 1)
                        print("point1 = %d ,point2 = %d"%(cfg.LINE_POINT_ONE, cfg.LINE_POINT_TWO))
                except Exception as e:  # Поймать и распечатать ошибку
                    go.stop()  # Выход, остановка машины
                    self.cap_open = 0  # Закрытие флага
                    self.cap.release()  # Освобождение камеры
                    print('linepatrol_processing error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # Если выйти из режима следования по линии
                go.stop()  # Выход из следования по линии, остановка машины
                self.cap_open = 0  # Закрытие флага
                self.cap.release()  # Освобождение камеры
                break  # Выход из цикла

    def facefollow(self):
        """
        Обнаружение лиц и отслеживание камерой
        :return:
        """
        time.sleep(3)
        while True:
            if self.cap_open == 0:  # Камера не открыта
                try:
                    # self.cap = cv2.VideoCapture(0)  # Открытие камеры
                    self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                    self.cap_open = 1  # Установка флага открытия камеры
                    self.cap.set(3, 320)  # Установка ширины изображения равной 320 пикселям
                    self.cap.set(4, 320)  # Установка высоты изображения равной 320 пикселям
                    face_cascade = cv2.CascadeClassifier(
                        '/home/pi/work/python_src/face.xml')  # OpenCV классификатор для обнаружения лиц
                except Exception as e:
                    print('opencv camera open error:', e)
                    break
            else:
                try:
                    ret, frame = self.cap.read()  # Получение кадра с камеры
                    if ret == 1:  # Проверка работоспособности камеры
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Преобразование в оттенки серого
                        faces = face_cascade.detectMultiScale(gray)  # Обнаружение лиц
                        if len(faces) > 0:  # Если в видео есть контуры лиц
                            print('face found!')
                            for (x, y, w, h) in faces:
                                # Рисуем прямоугольник вокруг лица с зелеными границами
                                cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)
                                result = (x, y, w, h)
                                x_middle = result[0] + w / 2  # Центральная точка X
                                y_middle = result[1] + h / 2  # Центральная точка Y

                                self.X_pid.update(x_middle)  # Отправка данных X в PID для расчета выходного значения
                                self.Y_pid.update(y_middle)  # Отправка данных Y в PID для расчета выходного значения
                                # print("X_pid.output==%d" % self.X_pid.output)  # Печать выходного значения X
                                # print("Y_pid.output==%d" % self.Y_pid.output)  # Печать выходного значения Y
                                self.angle_X = math.ceil(
                                    self.angle_X + 1 * self.X_pid.output)  # Обновление угла X сервопривода, добавление определенного коэффициента к предыдущему углу и округление до целого числа
                                self.angle_Y = math.ceil(
                                    self.angle_Y + 0.8 * self.Y_pid.output)  # Обновление угла Y сервопривода, добавление определенного коэффициента к предыдущему углу и округление до целого числа

                                # Ограничение максимального угла X
                                # if self.angle_X > 180:
                                #     self.angle_X = 180
                                # Ограничение минимального угла X
                                # if self.angle_X < 0:
                                #     self.angle_X = 0
                                # Ограничение максимального угла Y
                                # if self.angle_Y > 180:
                                #     self.angle_Y = 180
                                # Ограничение минимального угла Y
                                # if self.angle_Y < 0:
                                #     self.angle_Y = 0
                                self.angle_X = min(180, max(0, self.angle_X))
                                self.angle_Y = min(180, max(0, self.angle_Y))
                                print("angle_X: %d" % self.angle_X)  # Печать угла X сервопривода
                                print("angle_Y: %d" % self.angle_Y)  # Печать угла Y сервопривода
                                servo.set(self.servo_X, self.angle_X)  # Установка угла X сервопривода
                                servo.set(self.servo_Y, self.angle_Y)  # Установка угла Y сервопривода
                    # cv2.imshow("capture", frame)  # Отображение изображения
                except Exception as e:  # Поймать и распечатать ошибку
                    go.stop()  # Выход, остановка машины
                    self.cap_open = 0  # Закрытие флага
                    self.cap.release()  # Освобождение камеры
                    print('facefollow error:', e)
            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # Если выйти из режима следования за лицом
                go.stop()  # Выход, остановка машины
                self.cap_open = 0  # Закрытие флага
                self.cap.release()  # Освобождение камеры
                # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'  # Команда для завершения видеотрансляции камеры
                # call("%s" % path_sh, shell=True)  # Запуск команды оболочки для завершения видеотрансляции камеры
                time.sleep(2)
            break  # Выход из цикла

    def colorfollow(self):
        """
        Следование камерой за цветом
        :return:
        """
        while True:
            if self.cap_open == 0:  # Камера не открыта
                # self.cap = cv2.VideoCapture(0)  # Открытие камеры
                self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                self.cap_open = 1  # Установка флага открытия камеры
                self.cap.set(3, 320)  # Установка ширины изображения равной 320 пикселям
                self.cap.set(4, 320)  # Установка высоты изображения равной 320 пикселям
            else:
                try:
                    ret, frame = self.cap.read()  # Получение кадра с камеры
                    if ret == 1:  # Проверка работоспособности камеры
                        frame = cv2.GaussianBlur(frame, (5, 5),0)  # Применение гауссового фильтра для размытия изображения
                        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  # Преобразование изображения в формат HSV для удобства цветового анализа
                        mask = cv2.inRange(hsv, cfg.COLOR_LOWER[cfg.COLOR_INDEX], cfg.COLOR_UPPER[cfg.COLOR_INDEX])  # Определение области, соответствующей выбранному цвету, путем использования диапазонов цветов
                        mask = cv2.erode(mask, None, iterations=2)  # Применение операции эрозии для улучшения контура объекта
                        mask = cv2.GaussianBlur(mask, (3, 3), 0)  # Применение гауссового фильтра для смягчения краев
                        res = cv2.bitwise_and(frame, frame, mask=mask)  # Объединение исходного изображения с маской

                        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Обнаружение контуров объектов

                        if len(cnts) > 0:  # Если найдены объекты
                            cnt = max(cnts, key=cv2.contourArea)  # Выбор наибольшего контура
                            (x, y), radius = cv2.minEnclosingCircle(cnt)  # Нахождение центра объекта и радиуса
                            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255),2)  # Рисование круга вокруг объекта
                            # print(int(x), int(y))

                            self.X_pid.update(x)  # Отправка данных X в PID для расчета выходного значения
                            self.Y_pid.update(y)  # Отправка данных Y в PID для расчета выходного значения
                            # print("X_pid.output==%d"%X_pid.output)  # Печать выходного значения X
                            # print("Y_pid.output==%d"%Y_pid.output)  # Печать выходного значения Y
                            self.angle_X = math.ceil(self.angle_X + 1 * self.X_pid.output)  # Обновление угла X сервопривода, добавление определенного коэффициента к предыдущему углу и округление до целого числа
                            self.angle_Y = math.ceil(self.angle_Y + 0.8 * self.Y_pid.output)  # Обновление угла Y сервопривода, добавление определенного коэффициента к предыдущему углу и округление до целого числа

                            # Ограничение максимального угла X
                            if self.angle_X > 180:
                                self.angle_X = 180
                            # Ограничение минимального угла X
                            if self.angle_X < 0:
                                self.angle_X = 0
                            # Ограничение максимального угла Y
                            if self.angle_Y > 180:
                                self.angle_Y = 180
                            # Ограничение минимального угла Y
                            if self.angle_Y < 0:
                                self.angle_Y = 0
                            self.angle_X = min(180, max(0, self.angle_X))
                            self.angle_Y = min(180, max(0, self.angle_Y))
                            print("angle_X: %d" % self.angle_X)  # Печать угла X сервопривода
                            print("angle_Y: %d" % self.angle_Y)  # Печать угла Y сервопривода
                            servo.set(self.servo_X, self.angle_X)  # Установка угла X сервопривода
                            servo.set(self.servo_Y, self.angle_Y)  # Установка угла Y сервопривода
                except Exception as e:  # Поймать и распечатать ошибку
                    go.stop()  # Выход, остановка машины
                    self.cap_open = 0  # Закрытие флага
                    self.cap.release()  # Освобождение камеры
                    print('colorfollow error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # Если выйти из режима следования за цветом
                go.stop()  # Выход, остановка машины
                self.cap_open = 0  # Закрытие флага
                self.cap.release()  # Освобождение камеры
                break  # Выход из цикла

    def decodeDisplay(self, image):
        """
        Распознавание QR-кодов
        :param image:return: кадр с камеры
        :return: изображение с распознанным QR-кодом
        """
        barcodes = pyzbar.decode(image)
        if barcodes == []:
            cfg.BARCODE_DATE = None
            cfg.BARCODE_TYPE = None

        else:
            for barcode in barcodes:
                # Извлечение границ QR-кода.
                # Рисуем границы QR-кода на изображении
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Данные QR-кода представлены в виде байтового объекта, поэтому если мы хотим вывести их на изображение, нужно сначала преобразовать их в строку
                cfg.BARCODE_DATE = barcode.data.decode("utf-8")
                cfg.BARCODE_TYPE = barcode.type

                # Рисуем данные QR-кода и его тип на изображении
                text = "{} ({})".format(cfg.BARCODE_DATE, cfg.BARCODE_TYPE)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 125), 2)

                # Вывод данных QR-кода и его типа на терминал
                # print("[INFO] Найден {} баркод: {}".format(cfg.BARCODE_TYPE, cfg.BARCODE_DATE))


        return image

    def qrcode_detection(self):
        """
        Движение камеры для распознавания QR-кодов
        :return:
        """
        while True:
            if self.cap_open == 0:  # Камера не открыта
                # self.cap = cv2.VideoCapture(0)  # Открытие камеры
                self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                self.cap_open = 1  # Установка флага открытия камеры
            else:
                try:
                    ret, frame = self.cap.read()  # Получение кадра с камеры
                    if ret == 1:  # Проверка работоспособности камеры
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Преобразование в оттенки серого
                        img = self.decodeDisplay(gray)  # Распознавание QR-кода
                    # cv2.imshow("qrcode", img)  # Отображение изображения
                except Exception as e:  # Поймать и распечатать ошибку
                    go.stop()  # Выход, остановка машины
                    self.cap_open = 0  # Закрытие флага
                    self.cap.release()  # Освобождение камеры
                    print('ошибка qrcode_detection:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # Если выйти из режима распознавания QR-кодов
                go.stop()  # Выход, остановка машины
                self.cap_open = 0  # Закрытие флага
                self.cap.release()  # Освобождение камеры
                break  # Выход из цикла

    def run(self):
        """
        Переключение режимов камеры
        :return:
        """
        while True:
            if cfg.CAMERA_MOD == 1:  # Режим следования по линии
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Сохранение текущего значения скорости
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                cfg.LEFT_SPEED = 45  # Уменьшение скорости для режима следования по линии
                cfg.RIGHT_SPEED = 45
                self.linepatrol_processing()
            elif cfg.CAMERA_MOD == 2:  # Режим следования за лицом
                self.facefollow()
            elif cfg.CAMERA_MOD == 3:  # Режим следования за цветом
                self.colorfollow()
            elif cfg.CAMERA_MOD == 4:  # Режим распознавания QR-кодов
                self.qrcode_detection()
            else:
                pass
            time.sleep(0.05)