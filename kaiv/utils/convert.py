# That script converts a list of vertices (x1 y1 x2 y2 x3 y3 x4 y4) to boxes (cx cy w h)
import cv2
import numpy as np
import os
import shutil

def parse_vertices(path):
    boxes = []
    for line in open(path, 'r'):
        i, x1, y1, x2, y2, x3, y3, x4, y4 = [float(x) for x in line.split()]
        w = (max(x1, x2, x3, x4) - min(x1, x2, x3, x4)) / 2
        h = (max(y1, y2, y3, y4) - min(y1, y2, y3, y4)) / 2
        cx = (max(x1, x2, x3, x4) + min(x1, x2, x3, x4)) / 2
        cy = (max(y1, y2, y3, y4) + min(y1, y2, y3, y4)) / 2
        boxes.append(f"{int(i)} {cx} {cy} {w} {h}")
    return boxes


SRC_DIR = "../../datasets/cubes"
DST_DIR = "../../datasets/cubes_boxes"
files = [f for f in os.listdir(SRC_DIR) if os.path.isfile(os.path.join(SRC_DIR, f))]

try: os.mkdir(DST_DIR)
except FileExistsError: pass

for file in files:
    src_file = os.path.join(SRC_DIR, file)
    dst_file = os.path.join(DST_DIR, file)
    if src_file.endswith("txt"):
        boxes = parse_vertices(src_file)
        with open(dst_file, 'w') as f:
            f.writelines(boxes)
    else:
        shutil.copy(src_file, dst_file)

    





