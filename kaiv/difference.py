import cv2
import numpy as np
from ultralytics import YOLO
import os
import random


TEXT_SIZE = 0.75
TEXT_THICKNESS = 2
TEXT_FACE = cv2.FONT_HERSHEY_SIMPLEX

TARGET_DIM = 800
SRC_DIR = "../datasets/eval_circles_boxes"
MODEL_SAVE = "./runs/detect/train/weights/best.pt"

model = YOLO(MODEL_SAVE)

if __name__ != '__main__': exit()

LABELS = [
    "circle", 
    "box",
    #"int", 
    #"geo", 
    #"pro", 
    #"non"
    ]

COLORS = [
    (47, 70, 238),
    (148, 155, 255),
    (27, 106, 255),
    (20, 181, 252),
    (61, 206, 207),
    ]

IMAGE_SIZE = (1, 1)

def relative_to_absolute(coords):
    cx, cy, w, h = coords
    global IMAGE_SIZE
    cx = float(cx)
    cy = float(cy)
    w = float(w)
    h = float(h)
    sx = (cx - w) * IMAGE_SIZE[0]
    sy = (cy - h) * IMAGE_SIZE[1]
    ex = (cx + w) * IMAGE_SIZE[0]
    ey = (cy + h) * IMAGE_SIZE[1]
    return int4((sx, sy, ex, ey))

def parse_label(path):
    boxes = []
    for line in open(path, 'r'):
        i, cx, cy, w, h = line.split()
        boxes.append([
            int(i),
            relative_to_absolute((cx, cy, w, h))
            ])
    return boxes

def parse_result(data):
    boxes = []
    for box in data.boxes:
        boxes.append([
            int(box.cls),
            relative_to_absolute(box.xywhn.cpu().numpy().reshape(-1))
            ])
    return boxes

def int4(coords):
    return int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])

def draw_boxes(img, boxes):
    for box in boxes:
        i, coords = box
        sx, sy, ex, ey = coords
        cv2.rectangle(img, (sx, sy), (ex, ey), COLORS[i], 2)
    for box in boxes:
        i, coords = box
        sx, sy, ex, ey = coords
        text_size, _ = cv2.getTextSize(LABELS[i], TEXT_FACE, TEXT_SIZE, TEXT_THICKNESS)
        cv2.rectangle(img, (sx, sy), (sx + text_size[0], sy - text_size[1]), COLORS[i], -1)
        cv2.putText(img, LABELS[i], (sx, sy), TEXT_FACE, TEXT_SIZE, (0, 0, 0), TEXT_THICKNESS)
    return img

try:
    while True:
        files = [f for f in os.listdir(SRC_DIR) if os.path.isfile(os.path.join(SRC_DIR, f)) and f.endswith("jpg")]

        path = files[int(random.random() * (len(files) - 1))].replace(".jpg", "")
        img_path = f'{SRC_DIR}/{path}.jpg'
        label_path = f'{SRC_DIR}/{path}.txt'

        image = cv2.imread(img_path)
        aspect = image.shape[1] / image.shape[0]
        if aspect < 1:
            IMAGE_SIZE = (int(TARGET_DIM * aspect), TARGET_DIM)
        else:
            IMAGE_SIZE = (TARGET_DIM, int(TARGET_DIM / aspect))
        image = cv2.resize(image, IMAGE_SIZE)

        boxes = parse_label(label_path)
        image = draw_boxes(image, boxes)
        cv2.imshow("given", image)

        result = model(img_path)
        predicted_image = result[0].orig_img
        predicted_image = cv2.resize(predicted_image, IMAGE_SIZE)
        predicted_boxes = parse_result(result[0])
        predicted_image = draw_boxes(predicted_image, predicted_boxes)
        cv2.imshow("nn_output", predicted_image)

        k = cv2.waitKey(0)
except KeyboardInterrupt:
    exit()