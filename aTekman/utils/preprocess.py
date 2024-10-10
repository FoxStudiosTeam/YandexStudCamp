import cv2

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (640, 640))  # Размер, подходящий для YOLOv5
    img = img / 255.0  # Нормализация
    return img