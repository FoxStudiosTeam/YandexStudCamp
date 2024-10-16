from ultralytics import YOLO
import torch
import cv2
import numpy as np
import time
import os

model = YOLO("yolov8n.pt")
model.train(
    data='train.yaml', epochs=8, batch=24,
    #imgsz=960,
    #workers=0,
    hsv_h= 0.02,
    hsv_s= 0,
    hsv_v= 0,
    degrees= 0,
    translate= 0,
    scale= 0,
    shear= 0.08,
    perspective= 0.0,
    flipud= 0.0,
    fliplr= 0.0,
    bgr= 0.0,
    mosaic= 0,
    mixup= 0,
    copy_paste= 0,
    erasing= 0.04,
    crop_fraction= 0.04
    )