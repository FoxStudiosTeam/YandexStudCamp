import cv2
import numpy as np
from camera_capture import CameraCapture

class YOLOv8:
    def __init__(self):
        self.net = cv2.dnn.readNetFromDarknet("yolov8.cfg", "yolov8.weights")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def detect(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())
        return outputs

    def non_max_suppression(self, features):
        boxes = []
        scores = []
        classes = []
        for feature in features:
            scores.append(feature[:, 4])
            classes.append(feature[:, 5])
            boxes.append(feature[:, :4])
        indices = cv2.dnn.NMSBoxes(boxes, scores, 0.5, 0.4)
        return [boxes[i] for i in indices], [scores[i] for i in indices], [classes[i] for i in indices]

def main():
    camera = CameraCapture()
    yolov8 = YOLOv8()

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        outputs = yolov8.detect(frame)
        boxes, scores, classes = yolov8.non_max_suppression(outputs)

        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{yolov8.classes[int(classes[i])]} {scores[i]:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
