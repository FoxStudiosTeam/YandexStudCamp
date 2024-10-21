import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
import cv2
import numpy as np
from PIL import Image
from train import RectangleNet




model = RectangleNet()
model.load_state_dict(torch.load('MSE19.pth', weights_only=True))
model.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((128, 128))
])


with torch.no_grad():
    for filename in os.listdir('dataset'):
        if not filename.endswith('.jpg'):
            continue
        # Пример на одном изображении
        img = cv2.imread('dataset/' + filename)
        image = transform(img).unsqueeze(0)
        output = model(image)
        coords = output.squeeze().numpy()

        cv2.circle(img, (int(coords[0] * 256), int(coords[1] * 256)), 5, (0, 0, 255), -1)
        cv2.imshow('Image', img)
        print("Предсказанные координаты:", coords)
        cv2.waitKey(0)