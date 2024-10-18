# utils.py

import os
import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt

def prepare_data(data_dir):
    """
    Подготовка данных: разделение на обучающую и тестовую выборки.
    """
    # Здесь вы можете добавить код для подготовки данных
    # Например, создание поддиректорий train/ и test/ и перемещение изображений
    print(f"Preparing data in directory: {data_dir}")
    # Добавьте вашу логику здесь

def load_model(model_path):
    """
    Загрузка предобученной модели из указанного пути.
    """
    if os.path.exists(model_path):
        model = YOLO(model_path)
        print(f"Model loaded from {model_path}")
        return model
    else:
        raise FileNotFoundError(f"Model file not found at {model_path}")

def visualize_results(results):

    for result in results:
        # result по идее должен содержать изображение и предсказания
        img = result.orig_img
        predictions = result.pred
        # Визуализация
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title("Predictions")
        plt.show()

def resize_image(image, size):

    return cv2.resize(image, size)

def normalize_image(image):

    return image / 255.0

