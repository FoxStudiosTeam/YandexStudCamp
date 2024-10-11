import cv2
from aTekman.yolov8 import YOLOv8


class CameraCapture:
    def __init__(self, ip_camera_url):
        self.video_capture = cv2.VideoCapture(ip_camera_url)

    def read(self):
        ret, frame = self.video_capture.read()
        return ret, frame


def capture_cameras():
    # IP camera URL (replace with your camera's URL)
    ip_camera_url_left = "rtsp://Admin:rtf123@192.168.2.250/251:554/1/1"
    ip_camera_url_right = "rtsp://Admin:rtf123@192.168.2.251/251:554/1/1"

    # Create camera capture objects
    camera_left = CameraCapture(ip_camera_url_left)
    camera_right = CameraCapture(ip_camera_url_right)

    return camera_left, camera_right


# Check if the camera connection is successful
def check_camera_connection(camera_left, camera_right):
    if not camera_left.video_capture.isOpened() or not camera_right.video_capture.isOpened():
        print("Ошибка: Не удалось подключиться к IP-камере")
        exit(1)


# Capture a frame from the left camera
def capture_frame_left(camera_left):
    ret_left, frame_left = camera_left.read()
    if not ret_left:
        print("Ошибка: Не удалось захватить кадр с левой камеры")
        return None
    return frame_left


# Capture a frame from the right camera
def capture_frame_right(camera_right):
    ret_right, frame_right = camera_right.read()
    if not ret_right:
        print("Ошибка: Не удалось захватить кадр с правой камеры")
        return None
    return frame_right
