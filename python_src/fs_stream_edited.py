from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO
import time
import threading

# local file
from difference import draw_boxes, parse_result

TEXT_SIZE = 0.75
TEXT_THICKNESS = 2
TEXT_FACE = cv2.FONT_HERSHEY_SIMPLEX

LABELS = [
    "circle",
    "box",
    # "int",
    # "geo",
    # "pro",
    # "non"
]

COLORS = [
    (47, 70, 238),
    (148, 155, 255),
    (27, 106, 255),
    (20, 181, 252),
    (61, 206, 207),
]

IMAGE_SIZE = (1, 1)

fs_stream_edited_app = Flask(__name__)

# MODEL = YOLO("/home/pi/work/python_src/best.pt")
MODEL = YOLO("C:/Users/Hauptsturmfuhrer/Desktop/project/YandexStudCamp/python_src/best(3).pt")
def predict(frame):
    return MODEL.predict(frame)[0]


@fs_stream_edited_app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        result = predict(frame)
        boxes = parse_result(result)
        if len(boxes) == 0:
            cv2.putText(frame, str("NO OBJECTS FOUND"), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        image = draw_boxes(frame, boxes)
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        # time.sleep(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@fs_stream_edited_app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

threading.Thread(target=fs_stream_edited_app.run, args=('0.0.0.0','8080')).start()
