from flask import Flask, Response
import cv2

import threading

camera_streamer_app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture("http://192.168.2.81:8080?action=stream")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@camera_streamer_app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

thread = threading.Thread(target=camera_streamer_app.run, args=('0.0.0.0', '8080'))

thread.start()