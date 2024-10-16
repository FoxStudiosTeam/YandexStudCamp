# This file merges two datasets into one
# ONLY WORK WITH BOX LABELS!
import cv2
import numpy as np
import os
import shutil

# vec![(path, variants)]
SRC_DIRS = [
    ("../../datasets/spheres_boxes", 1),
    ("../../datasets/cubes_boxes", 1),
]

DST_DIR = "../../datasets/merged_circles_boxes"

try: os.mkdir(DST_DIR)
except FileExistsError: pass


def cp_with_variant_offset(src_file, dst_file, offset):
    data = []
    for line in open(src_file, 'r'):
        try:
            i, cx, cy, w, h = [float(x) for x in line.split()]
            data.append(f"{int(i) + offset} {cx} {cy} {w} {h}")
        except:
            print(f"Labels must be boxes! File: {src_file} Please, delete it manually")
    with open(dst_file, 'w') as f:
        f.writelines(data)

variant_offset = 0
for (src_dir, variants) in SRC_DIRS:
    files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    for file in files:
        src_file = os.path.join(src_dir, file)
        dst_file = os.path.join(DST_DIR, file)
        if src_file.endswith("txt"):
            cp_with_variant_offset(src_file, dst_file, variant_offset)
        else:
            shutil.copy(src_file, dst_file)
    variant_offset += variants




























