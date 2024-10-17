import os
from ultralytics import YOLO

# Конфигурация
DATASET_PATH = 'data/dataset.yaml'
MODEL_PATH = 'models/yolov8_model.pt'
EPOCHS = 50
BATCH_SIZE = 16

def train_model():

    model = YOLO('yolov8n.pt')
    results = model.train(data=DATASET_PATH, epochs=EPOCHS, batch=BATCH_SIZE)

    print("Обучение завершено. Результаты:")
    print(results)

if __name__ == '__main__':
    train_model()
