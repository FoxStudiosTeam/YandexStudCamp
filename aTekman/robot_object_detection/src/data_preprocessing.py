import os
import cv2
import numpy as np
from src.config import IMAGE_WIDTH, IMAGE_HEIGHT

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
            images.append(img)
    return np.array(images)

def preprocess_labels(labels):
    #код для предобработки меток return labels
