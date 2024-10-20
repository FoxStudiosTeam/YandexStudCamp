import cv2
import numpy as np
import random
import os



src_points = np.array([[399,88], [1500, 150], [1460, 962], [383, 953]], dtype='float32')


for file in os.listdir("./src_imgs"):
    print(file)
    if file.endswith(".jpg"):
        image = cv2.imread(f'./src_imgs/{file}')
        dst_points = np.array([[0, 0], [800, 0], [800, 600], [0, 600]], dtype='float32')
        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        warped_image = cv2.warpPerspective(image, matrix, (800, 600))
        cv2.imwrite(f'./converted/{file}', warped_image)