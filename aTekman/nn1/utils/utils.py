import numpy as np

def iou(box1, box2):
    # Calculate the intersection over union (IOU) between two bounding boxes
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    intersection = max(0, min(x2, x4) - max(x1, x3)) * max(0, min(y2, y4) - max(y1, y3))
    union = (x2 - x1) * (y2 - y1) + (x4 - x3) * (y4 - y3) - intersection
    return intersection / union

def non_max_suppression(boxes, scores, threshold):
    # Implement non-maximum suppression algorithm
    # ...
    pass
