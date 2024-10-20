from ultralytics import YOLO
import torch
import cv2
import numpy as np
import time
import os


model = YOLO("./runs/segment/train/weights/best.pt")




r = model("../datasets/eval_upper_camera_polygon/1frame+0 (2).jpg")

img = cv2.imread("../datasets/eval_upper_camera_polygon/1frame+0 (2).jpg")

IMG_SIZE = (1920, 1080)

lu = None
ru = None
rd = None
ld = None


def dist_squared(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

for vertex_coordinates in r[0].masks.xy[0]:
    vp = (vertex_coordinates[0], vertex_coordinates[1])
    lu_d = dist_squared(vp, (0, 0))
    if lu == None or lu[0] > lu_d:
        lu = (lu_d, vp)
    ru_d = dist_squared(vp, (IMG_SIZE[0], 0))
    if ru == None or ru[0] > ru_d:
        ru = (ru_d, vp)
    rd_d = dist_squared(vp, (IMG_SIZE[0], IMG_SIZE[1]))
    if rd == None or rd[0] > rd_d:
        rd = (rd_d, vp)
    ld_d = dist_squared(vp, (0, IMG_SIZE[1]))
    if ld == None or ld[0] > ld_d:
        ld = (ld_d, vp)

cv2.circle(img, [int(lu[1][0]), int(lu[1][1])], 5, (0, 0, 255), -1)
cv2.circle(img, [int(ru[1][0]), int(ru[1][1])], 5, (0, 0, 255), -1)
cv2.circle(img, [int(rd[1][0]), int(rd[1][1])], 5, (0, 0, 255), -1)
cv2.circle(img, [int(ld[1][0]), int(ld[1][1])], 5, (0, 0, 255), -1)

cv2.imwrite("test.jpg", img)