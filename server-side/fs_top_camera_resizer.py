import cv2
import numpy as np
import torch

from train import RectangleNet
import torchvision.transforms as transforms

def resize_field(img):

    model = RectangleNet()

    model.load_state_dict(torch.load("C:/Users/UrFU/Desktop/YandexStudCamp/server-side/MSE19.pth", weights_only=True, map_location=torch.device('cpu')))
    model.eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((128, 128))
    ])

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
    frame = cv2.warpPerspective(img, matrix, (800, 600))
    return frame