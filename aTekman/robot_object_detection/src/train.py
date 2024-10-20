import os
from ultralytics import YOLO
from config import EPOCHS, BATCH_SIZE


def train_model():
    model = YOLO('yolov8n.pt')  # И
    results = model.train(
        data='train.yaml',
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        # imgsz=960,
        hsv_h=0.4,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0,
        translate=0,
        scale=0,
        shear=0.08,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        bgr=0.0,
        mosaic=1.0,
        mixup=0,
        copy_paste=0,
        erasing=0.04,
        crop_fraction=0.04
    )

    print("Обучение завершено. Результаты:")
    print(results)

if __name__ == '__main__':
    train_model()
