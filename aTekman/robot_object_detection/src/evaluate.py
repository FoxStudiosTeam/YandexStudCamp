import os
import torch
from torchvision import transforms
from torchvision.ops import box_iou
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
import cv2
import matplotlib.pyplot as plt

from ultralytics import YOLO

# Конфигурация
MODEL_PATH = 'models/yolov8_model.pt'
TEST_IMAGES_DIR = 'data/split/test/'
LABELS_DIR = 'data/labels/'
RESULTS_DIR = 'results/metrics/'



def load_model(model_path):
    model = YOLO(model_path)
    return model


# Функция для получения предсказаний
def get_predictions(model, image):
    results = model(image)
    return results.pred[0]  # Предположим, что возвращается список предсказанных объектов


# Функция для вычисления метрик
def calculate_metrics(y_true, y_pred):
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    return precision, recall, f1


# Функция для визуализации результатов
def visualize_results(image, predictions, save_path):
    for pred in predictions:
        x1, y1, x2, y2, conf, cls = pred  # Распаковка предсказаний
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(image, f'Class: {int(cls)} Conf: {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 0, 0), 2)

    cv2.imwrite(save_path, image)


# Основная функция оценки
def load_annotations(label_path):
    pass


def evaluate():
    model = load_model(MODEL_PATH)
    all_y_true = []
    all_y_pred = []
    all_images = os.listdir(TEST_IMAGES_DIR)

    for image_name in all_images:
        image_path = os.path.join(TEST_IMAGES_DIR, image_name)
        image = cv2.imread(image_path)

        # Получаем предсказания
        predictions = get_predictions(model, image)

        # Например, в 'data/labels/image_name.txt'
        label_path = os.path.join(LABELS_DIR, image_name.replace('.jpg', '.txt'))
        y_true = load_annotations(label_path)
        y_pred = [pred[-1] for pred in predictions]  # Предсказанные классы all_y_true.extend(y_true)
        all_y_pred.extend(y_pred)

        # Визуализация результатов
        visualize_results(image, predictions, os.path.join(RESULTS_DIR, image_name))

    # Вычисление метрик
    precision, recall, f1 = calculate_metrics(all_y_true, all_y_pred)

    # Сохранение метрик
    with open(os.path.join(RESULTS_DIR, 'metrics.txt'), 'w') as f:
        f.write(f'Precision: {precision:.4f}\n')
        f.write(f'Recall: {recall:.4f}\n')
        f.write(f'F1 Score: {f1:.4f}\n')


if __name__ == '__main__':
    evaluate()
