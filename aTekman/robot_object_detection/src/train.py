import os
from ultralytics import YOLO
from config import EPOCHS, BATCH_SIZE
# Конфигурация
DATASET_PATH = 'data/split/test'
MODEL_PATH = 'models/yolov8n_model.pt'


def train_model():

    model = YOLO('yolov8n.pt')
    results = model.train(data=DATASET_PATH, epochs=EPOCHS, batch=BATCH_SIZE)

    print("Обучение завершено. Результаты:")
    print(results)

if __name__ == '__main__':
    train_model()
