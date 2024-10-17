# utils/models.py
import torch
import torch.nn as nn

class YOLOv8(nn.Module):
    def __init__(self):
        super(YOLOv8, self).__init__()
        self.model = torch.hub.load('ultralytics/yolov8', 'yolov8n')

    def forward(self, x):
        return self.model(x)

def load_yolov8_model():
    """
    Загрузка модели YOLOv8.

    Returns:
        YOLOv8: Модель YOLOv8.
    """
    model = YOLOv8()
    return model
