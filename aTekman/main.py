import cv2
from aTekman.yolov8 import YOLOv8

# Load the YOLOv8 model
yolov8 = YOLOv8(input_shape=(416, 416, 3), num_classes=80)

# Load the image
image = cv2.imread('image.jpg')

# Detect objects in the image
boxes, scores, classes = yolov8.detect_objects(image)

# Draw bounding boxes on the image
for box, score, class_id in zip(boxes, scores, classes):
    x, y, w, h = box
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(image, f'Class: {class_id}, Score: {score:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the output
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
