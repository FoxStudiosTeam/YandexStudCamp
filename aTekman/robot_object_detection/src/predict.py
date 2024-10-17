import cv2
import numpy as np
import joblib
import os
import logging
import argparse

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_yolo_model(weights_path, config_path):
    try:
        net = cv2.dnn.readNet(weights_path, config_path)
        logging.info("Модель YOLO успешно загружена.")
        return net
    except Exception as e:
        logging.error(f"Ошибка при загрузке модели YOLO: {e}")
        exit(1)


def load_image(image_path):
    try:
        image = cv2.imread(image_path)
        logging.info("Изображение успешно загружено.")
        return image
    except Exception as e:
        logging.error(f"Ошибка при загрузке изображения: {e}")
        exit(1)

def make_predictions(net, image):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)

    boxes, confidences, class_ids = [], [], []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Порог уверенности
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    final_boxes = [boxes[i[0]] for i in indices]
    final_confidences = [confidences[i[0]] for i in indices]
    final_class_ids = [class_ids[i[0]] for i in indices]

    return final_boxes, final_confidences, final_class_ids

def save_predictions(image, boxes, class_ids, output_path):
    """Сохранение предсказаний на изображении."""
    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        label = str(class_ids[i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_path, image)
    logging.info(f"Предсказания сохранены в {output_path}")

def main(weights_path, config_path, image_path, output_path):
    """Основная функция для выполнения предсказаний с использованием YOLO."""
    net = load_yolo_model(weights_path, config_path)
    image = load_image(image_path)
    boxes, confidences, class_ids = make_predictions(net, image)
    save_predictions(image, boxes, class_ids, output_path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Выполнение предсказаний с использованием модели YOLO.')
    parser.add_argument('weights_path', type=str, help='Путь к файлу с весами модели YOLO')
    parser.add_argument('config_path', type=str, help='Путь к файлу конфигурации модели YOLO')
    parser.add_argument('image_path', type=str, help='Путь к изображению для предсказания')
    parser.add_argument('output_path', type=str, help='Путь для сохранения изображения с предсказаниями')
    args = parser.parse_args()
    main(args.weights_path, args.config_path, args.image_path, args.output_path)
