from ultralytics import YOLO
import torch
import cv2
import numpy as np
import time
import os

model = YOLO("yolov8n.pt")
model.train(
    data='train.yaml',
    epochs=25,
    batch=16,
    task='detect',
    #imgsz=960,
    workers=16,
    save=True,
    optimizer="Adam",
    verbose=True,
    cos_lr=True,
    amp=True,
    fraction=0.6,
    momentum=0.937,
    weight_decay=0.0005,
    box=10,
    cls=0.7,
    kobj=2.0,
    label_smoothing=0.5,
    nbs=64,
    dropout=0.1,
    plots=True,

    augment=True,
    visualize=True,

    agnostic_nms=True,
    show=True,
    show_boxes=True,
    hsv_h=0.025,
    hsv_s=0.025,
    hsv_v=0.6,
    degrees=180,
    translate=0.25,
    scale=1.0,
    shear=180,
    perspective=0.001,
    fliplr=0.5,
    bgr=0.15,
    mosaic=1.0,
    copy_paste=1.0,
    copy_paste_mode='mixup',
    auto_augment="randaugment",
    erasing=0.5,
    crop_fraction=0.5,


    device="mps")

#mps -> Apple M