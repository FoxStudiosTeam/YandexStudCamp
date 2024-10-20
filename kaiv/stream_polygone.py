from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO
import time
import numpy as np

# local file
from difference import draw_boxes, parse_result


TEXT_SIZE = 0.75
TEXT_THICKNESS = 2
TEXT_FACE = cv2.FONT_HERSHEY_SIMPLEX

LABELS = [
    "circle", 
    "box",
    #"int", 
    #"geo", 
    #"pro", 
    #"non"
    ]

COLORS = [
    (47, 70, 238),
    (148, 155, 255),
    (27, 106, 255),
    (20, 181, 252),
    (61, 206, 207),
    ]

IMAGE_SIZE = (1, 1)


app = Flask(__name__)

MODEL = YOLO("./best.pt")

def predict(frame):
    return MODEL.predict(frame)[0]

@app.route('/')
def index():
    return render_template('index.html')


def dist_squared(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2


IMG_SIZE = (1920, 1080)

def generate_frames():
    cap = cv2.VideoCapture(3)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        r = predict(frame)
        image = frame[:][:][:]
        image_dots = frame
        if r.masks is not None:
            lu = None
            ru = None
            rd = None
            ld = None
            for vertex_coordinates in r.masks.xy[0]:
                vp = (vertex_coordinates[0], vertex_coordinates[1])
                cv2.circle(image_dots, [int(vertex_coordinates[0]), int(vertex_coordinates[1])], 5, (0, 0, 255), -1)
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
            src_points = np.array([lu[1], ru[1], rd[1], ld[1]], dtype='float32')
            dst_points = np.array([[0, 0], [800, 0], [800, 600], [0, 600]], dtype='float32')
            matrix = cv2.getPerspectiveTransform(src_points, dst_points)
            image = cv2.warpPerspective(frame, matrix, (800, 600))

        #boxes = parse_result(result)
        #if len(boxes) == 0:
        #    cv2.putText(frame, str("NO OBJECTS FOUND"), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #image = draw_boxes(frame, boxes)
        #ret, buffer = cv2.imencode('.jpg', image)
        #frame = buffer.tobytes()
        #cv2.circle(frame, (100, 100), 50, (0, 0, 255), -1)

        try:
            concated = cv2.vconcat([image, cv2.resize(image_dots, (800, 600))])
            ret, buffer = cv2.imencode('.jpg', concated)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
