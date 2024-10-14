# coding:utf-8
"""
Скрипт управления WiFi-роботом с видеосвязью для Raspberry Pi
Автор: Sence
Права принадлежат компании XiaoR Technologies (г. Шэньчжэнь, Китай, www.xiao-r.com); форум WIFI роботов www.wifi-robots.com
Данный код может быть свободно модифицирован, однако запрещено его использование в коммерческих целях!
Данный код защищен авторским правом на программное обеспечение, любые нарушения будут преследоваться по закону!
"""
"""
@version: python3.7
@Author  : xiaor
@Explain : Настройка GPIO для Raspberry Pi
@contact :
@Time    :2020/05/09
@File    :xr_gpio.py
@Software: PyCharm
"""

import RPi.GPIO as GPIO

# Настройки для пинов
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Пины для пьезоизлучателя
BUZZER = 10

# Настройки для моторов
ENA = 13  	# L298N Enable A
ENB = 20  	# L298N Enable B
IN1 = 16  	# Мотор интерфейс 1
IN2 = 19  	# Мотор интерфейс 2
IN3 = 26  	# Мотор интерфейс 3
IN4 = 21  	# Мотор интерфейс 4

# Настройки для ультразвукового датчика
ECHO = 4  	# Приемник ультразвукового датчика
TRIG = 17  	# Передатчик ультразвукового датчика

# Настройки для инфракрасных датчиков
IR_R = 18  	# Инфракрасный датчик справа
IR_L = 27  	# Инфракрасный датчик слева
IR_M = 22  	# Инфракрасный датчик посередине
IRF_R = 25  # Инфракрасный датчик следования справа
IRF_L = 1  # Инфракрасный датчик следования слева

# Инициализация пинов
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
ENA_pwm = GPIO.PWM(ENA, 1000)
ENA_pwm.start(0)
ENA_pwm.ChangeDutyCycle(100)
ENB_pwm = GPIO.PWM(ENB, 1000)
ENB_pwm.start(0)
ENB_pwm.ChangeDutyCycle(100)

# Инициализация инфракрасных датчиков
GPIO.setup(IR_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Инициализация ультразвукового датчика
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)  			# Настройка вывода для ультразвукового модуля
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  	# Настройка входа для ультразвукового модуля

# Инициализация пьезоизлучателя
GPIO.setup(BUZZER, GPIO.OUT, initial=GPIO.LOW)			# Настройка выхода для пьезоизлучателя

def digital_write(gpio, status):
    """
    Установить уровень сигнала на пине gpio
    Аргументы: gpio - номер пина, статус - значение состояния (True - высокий уровень, False - низкий уровень)
    """
    GPIO.output(gpio, status)

def digital_read(gpio):
    """
    Прочитать уровень сигнала на пине gpio
    """
    return GPIO.input(gpio)

def ena_pwm(pwm):
    """
    Установить PWM на пине ENA
    """
    ENA_pwm.ChangeDutyCycle(pwm)

def enb_pwm(pwm):
    """
    Установить PWM на пине ENB
    """
    ENB_pwm.ChangeDutyCycle(pwm)
