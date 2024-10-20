# This file merges two datasets into one
# ONLY WORK WITH BOX LABELS!
import cv2
import numpy as np
import os
import shutil

# vec![(path, variants)]
SRC_DIRS = [
    ("../../datasets/spheres", 1),
    ("../../datasets/cubes", 1),
]

DST_DIR = "../../datasets/train_dataset"

try: os.mkdir(DST_DIR)
except FileExistsError: pass


def cp_with_variant_offset(src_file, dst_file, offset):
    data = []
    for line in open(src_file, 'r'):
        i, p = line.split(" ", 1)
        data.append(f"{int(i) + offset} {p}")
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




























