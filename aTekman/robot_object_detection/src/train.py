import os
from ultralytics import YOLO
from config import EPOCHS, BATCH_SIZE


def train_model():
    model = YOLO('C:\\Users\\weednw\\PycharmProjects\\YandexStudCamp\\aTekman\\robot_object_detection\\src\\runs\\detect\\train2\\weights\\best.pt')
    results = model.train(
        data='train.yaml',
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        hsv_h=0.6,
        hsv_s=0.2,
        hsv_v=0.4,
        degrees=0,
        translate=0.3,
        scale=0.5,
        shear=0.2,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        bgr=0.0,
        mosaic=1.0,
        mixup=0.6,
        copy_paste=0.2,
        auto_augment = 'randaugment',
        erasing=0.3,
        crop_fraction=0.04
    )

    print("Обучение завершено. Результаты:")
    print(results)

if __name__ == '__main__':
    train_model()
