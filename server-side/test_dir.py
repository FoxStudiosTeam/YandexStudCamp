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
model.load_state_dict(torch.load('C:/Users/Hauptsturmfuhrer/Desktop/project/YandexStudCamp/server-side/MSE19.pth', weights_only=True))
model.eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((128, 128))
])


with torch.no_grad():
    for filename in os.listdir('C:/Users/Hauptsturmfuhrer/Desktop/project/YandexStudCamp/test cut/test_dir'):
        if not filename.endswith('.jpg'):
            continue
        img = cv2.imread('C:/Users/Hauptsturmfuhrer/Desktop/project/YandexStudCamp/test cut/test_dir/' + filename)
        image = cv2.resize(img, (256, 256))
        height, width, _ = image.shape
        center_x, center_y = width // 2, height // 2
        top_left = image[0:center_y, 0:center_x]
        top_right = image[0:center_y, center_x:width]
        top_right = cv2.flip(top_right, 1)
        bottom_right = image[center_y:height, center_x:width]
        bottom_right = cv2.flip(bottom_right, -1)
        bottom_left = image[center_y:height, 0:center_x]
        bottom_left = cv2.flip(bottom_left, 0)
        images = [transform(top_left), transform(top_right), transform(bottom_right), transform(bottom_left)]
        images_batch = torch.stack(images)
        output = model(images_batch)
        output = output.detach().numpy()
        tl = output[0]
        tl = tl * 0.5
        tr = output[1]
        tr = tr * 0.5
        tr[0] = 1 - tr[0]
        br = output[2]
        br = br * 0.5
        br = 1 - br
        bl = output[3]
        bl = bl * 0.5
        bl[1] = 1 - bl[1]

        img_size = img.shape[:2][::-1]

        src_points = np.array([tl * img_size, tr * img_size, br * img_size, bl * img_size], dtype='float32')
        dst_points = np.array([[0, 0], [800, 0], [800, 600], [0, 600]], dtype='float32')
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        norm = cv2.warpPerspective(img, matrix, (800, 600))

        cv2.circle(img, (int(tl[0] * img_size[0]), int(tl[1] * img_size[1])), 5, (0, 0, 255), -1)
        cv2.circle(img, (int(tr[0] * img_size[0]), int(tr[1] * img_size[1])), 5, (0, 0, 255), -1)
        cv2.circle(img, (int(br[0] * img_size[0]), int(br[1] * img_size[1])), 5, (0, 0, 255), -1)
        cv2.circle(img, (int(bl[0] * img_size[0]), int(bl[1] * img_size[1])), 5, (0, 0, 255), -1)


        # cv2.imshow('Image', img)
        cv2.imshow('Norm', norm)

        cv2.waitKey(0)