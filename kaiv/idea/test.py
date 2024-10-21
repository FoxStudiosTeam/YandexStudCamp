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
    file = "img.jpg"
    img = cv2.imread(file)
    image = cv2.resize(img, (256, 256))

    height, width, _ = image.shape

    center_x, center_y = width // 2, height // 2

    top_left = image[0:center_y, 0:center_x]
    #tl = (label[0] * 2, label[1] * 2)

    top_right = image[0:center_y, center_x:width]
    #tr = ((1 - label[2]) * 2, label[3] * 2)
    top_right = cv2.flip(top_right, 1)

    bottom_right = image[center_y:height, center_x:width]
    #br = ((1 - label[4]) * 2, (1 - label[5]) * 2)
    bottom_right = cv2.flip(bottom_right, -1)

    bottom_left = image[center_y:height, 0:center_x]
    #bl = (label[6] * 2, (1 - label[7]) * 2)
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
    print(tl, tr, br, bl)
    cv2.circle(img, (int(tl[0] * 512), int(tl[1] * 512)), 5, (0, 0, 255), -1)
    cv2.circle(img, (int(tr[0] * 512), int(tr[1] * 512)), 5, (0, 0, 255), -1)
    cv2.circle(img, (int(br[0] * 512), int(br[1] * 512)), 5, (0, 0, 255), -1)
    cv2.circle(img, (int(bl[0] * 512), int(bl[1] * 512)), 5, (0, 0, 255), -1)
    cv2.imshow('Input image', img)
    img_size = img.shape[:2][::-1]
    src_points = np.array([tl * img_size, tr * img_size, br * img_size, bl * img_size], dtype='float32')
    dst_points = np.array([[0, 0], [800, 0], [800, 600], [0, 600]], dtype='float32')
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    norm = cv2.warpPerspective(img, matrix, (800, 600))
    cv2.imshow('Normalized image', norm)
    cv2.waitKey(0)




        