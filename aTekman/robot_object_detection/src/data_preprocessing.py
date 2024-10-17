import os
import cv2
import numpy as np
from config import IMAGE_WIDTH, IMAGE_HEIGHT

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
            images.append(img)
    return np.array(images)

def preprocess_labels(labels):
    label_map = {label: idx for idx, label in enumerate(set(labels))}
    numeric_labels = np.array([label_map[label] for label in labels])
    return numeric_labels
