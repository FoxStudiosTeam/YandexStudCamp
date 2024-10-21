import cv2
import numpy as np
import os


def undistort_fisheye_video(input_video_path):


    # Открываем входное видео
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print(f"Не удалось открыть видео: {input_video_path}")
        return

    # Получаем свойства видео


    print(f"Разрешение видео: {frame_width}x{frame_height}")
    print(f"FPS: {fps}")
    print(f"Всего кадров: {total_frames}")

    # ПАРАМЕТРЫ КАМЕРЫ (замените на ваши собственные значения)
    # Для примера используются приблизительные значения
    # Матрица камеры (фокусное расстояние и центр)


    # Коэффициенты дисторсии (k1, k2, p1, p2, k3)
    # Для рыбьего глаза обычно используются искажения высокого порядка
    # Примерные значения

    # Получаем оптимальную новую матрицу камеры без изменения поля зрения

    # Предварительно инициализируем карту для коррекции искажений

    frame_count = 0
    out = None  # Инициализация VideoWriter

    output_video_path = "frame"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Все кадры прочитаны.")
            break

        # Применяем коррекцию искажений

        try:
            cv2.imwrite(f'{output_video_path}+{frame_count}.jpg', undistorted_frame)
            #out.write(undistorted_frame)
        except Exception as e:
            print(f"Предупреждение: Не удалось записать кадр {frame_count}. Ошибка: {e}")


        frame_count += 1

if __name__ == "__main__":
    # Укажите путь к вашему входному видео и желаемый путь для выходного видео
    input_video = "rtsp://Admin:rtf123@192.168.2.250/251:554/1/1"  # Замените на ваш файл

    #output_video = "corrected_video.avi"  # Замените на желаемое название


    undistort_fisheye_video(input_video)
