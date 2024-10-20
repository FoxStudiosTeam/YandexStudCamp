import cv2
import numpy as np
import random
import os
image = cv2.imread('./src_imgs/frame+10 (5).jpg')

INPUT_SIZE = [1920, 1080]

SRC_POINTS = np.array([[399,88], [1500, 150], [1460, 962], [383, 953]], dtype='float32')
LABEL_POINTS = [[399,88], [1500, 150], [1460, 962], [383, 953]]

ORIGIN_POITNS = [
    [397, 109],
    [1525, 109],
    [1525, 981],
    [397, 981]
]

MAX_OFFSET = 35

VARIANTS = 3


for file in os.listdir("./src_imgs"):
    if file.endswith(".jpg"):
        image = cv2.imread(f'./src_imgs/{file}')
        for i in range(VARIANTS):
            #dst_points = np.array([[0, 0], [800, 0], [800, 600], [0, 600]], dtype='float32')
            #         matrix = cv2.getPerspectiveTransform(SRC_POINTS, dst_points)
            new_points = []
            for p in ORIGIN_POITNS:
                r = []
                for a in p:
                    r.append(a + random.randrange(-MAX_OFFSET, MAX_OFFSET+1))
                new_points.append(r)
            matrix = cv2.getPerspectiveTransform(SRC_POINTS, np.array(new_points, dtype='float32'))
            warped_image = cv2.warpPerspective(image, matrix, (1920, 1080))
            label = [0]
            for p in LABEL_POINTS:
                point_homogeneous = np.array([p[0], p[1], 1])
                transformed_point_homogeneous = matrix @ point_homogeneous
                transformed_point = [0, 0]
                if transformed_point_homogeneous[2] != 0:
                    a = transformed_point_homogeneous[:2] / transformed_point_homogeneous[2]
                    label.append(float(a[0]) / 1920)
                    label.append(float(a[1]) / 1080)
                else:
                    transformed_point = [float('inf'), float('inf')]
                    print("ZERO DIVISION")
                    exit()

                #cv2.circle(warped_image, transformed_point, 5, (0, 255, 0), -1)
            with open(f'./result/{i}{file.replace(".jpg", ".txt")}', 'w') as f:
                f.writelines([" ".join([str(s) for s in label])])
            cv2.imwrite(f'./result/{i}{file}', warped_image)