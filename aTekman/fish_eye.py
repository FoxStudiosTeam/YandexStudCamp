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
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Разрешение видео: {frame_width}x{frame_height}")
    print(f"FPS: {fps}")
    print(f"Всего кадров: {total_frames}")

    # ПАРАМЕТРЫ КАМЕРЫ (замените на ваши собственные значения)
    # Для примера используются приблизительные значения
    # Матрица камеры (фокусное расстояние и центр)
    K = np.array([[1000, 0, frame_width / 2],
                  [0, 1000, frame_height / 2],
                  [0, 0, 1]])

    # Коэффициенты дисторсии (k1, k2, p1, p2, k3)
    # Для рыбьего глаза обычно используются искажения высокого порядка
    # Примерные значения
    dist_coeffs = np.array([-0.3, 0.1, 0, 0, 0])

    # Получаем оптимальную новую матрицу камеры без изменения поля зрения
    new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist_coeffs, (frame_width, frame_height), 1,
                                               (frame_width, frame_height))

    # Предварительно инициализируем карту для коррекции искажений
    map1, map2 = cv2.initUndistortRectifyMap(K, dist_coeffs, None, new_K, (frame_width, frame_height), cv2.CV_16SC2)

    frame_count = 0
    out = None  # Инициализация VideoWriter

    output_video_path = "frame"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Все кадры прочитаны.")
            break

        # Применяем коррекцию искажений
        undistorted_frame = cv2.remap(frame, map1, map2, cv2.INTER_LINEAR)

        # Инициализируем VideoWriter после обработки первого кадра
 #       if frame_count == 0:
#            fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Попробуйте заменить на 'XVID' или 'MJPG'

            #print(f"VideoWriter инициализирован с разрешением: {frame_width}x{frame_height} и кодеком: {fourcc}")

        # Записываем исправленный кадр в выходное видео
        try:
            cv2.imwrite(f'{output_video_path}+{frame_count}.jpg', undistorted_frame)
            #out.write(undistorted_frame)
        except Exception as e:
            print(f"Предупреждение: Не удалось записать кадр {frame_count}. Ошибка: {e}")

        # Отображаем только исправленный кадр (опционально)
        cv2.imshow('Исправленное видео (Нажмите Q для выхода)', undistorted_frame)

        frame_count += 1
        if frame_count % 60 == 0:
            print(f"Обработано {frame_count}/{total_frames} кадров")

        # Проверка на нажатие клавиши 'q' для выхода
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Обработка прервана пользователем.")
            break

    # Освобождаем ресурсы
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
    print("Коррекция искажений завершена.")
    print(f"Исправленное видео сохранено как: {output_video_path}")


if __name__ == "__main__":
    # Укажите путь к вашему входному видео и желаемый путь для выходного видео
    input_video = "rtsp://Admin:rtf123@192.168.2.250/251:554/1/1"  # Замените на ваш файл

    #output_video = "corrected_video.avi"  # Замените на желаемое название


    undistort_fisheye_video(input_video)
