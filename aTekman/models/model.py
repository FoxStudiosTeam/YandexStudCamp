import torch
from models import DetectMultiBackend

class CustomYOLOv5:
    def __init__(self, weights='path/to/weights.pt', device='cpu'):
        self.model = DetectMultiBackend(weights, device=device)

    def predict(self, img):
        results = self.model(img)
        return results