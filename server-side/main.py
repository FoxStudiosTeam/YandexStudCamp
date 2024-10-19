import socket
from threading import Thread

import cv2
import numpy as np
from ultralytics import YOLO


class TcpServer:
    def __init__(self):
        self.client_socket = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", 2002))
        self.socket.listen(1)

        self.labels = [
            "circle",
            "box",
            # "int",
            # "geo",
            # "pro",
            # "non"
        ]

        self.colors = [
            (47, 70, 238),
            (148, 155, 255),
            (27, 106, 255),
            (20, 181, 252),
            (61, 206, 207),
        ]

        self.image_size = (1, 1)

        self.model = YOLO("./Artem_welll_01.pt")
        # MODEL = YOLO("C:/Users/Hauptsturmfuhrer/Desktop/project/YandexStudCamp/python_src/best(3).pt")

    def predict(self, frame):
        return self.model.predict(frame)[0]

    def validate(self, message, command):
        if message == "error":
            self.client_socket.send(command.encode())
        if message == "ok":
            pass

    def parse_result(self, data):
        classes_names = data.names
        classes = data.boxes.cls.cpu().numpy()
        boxes = data.boxes.xyxy.cpu().numpy().astype(np.int32)
        return classes_names, classes, boxes

    def down_cam(self) -> None:
        # cum = cv2.VideoCapture(f"{address[0]}:{address[1]}?action=stream")
        # cum = cv2.VideoCapture(f"http://192.168.2.81:8080/?action=stream")
        # cum = cv2.VideoCapture(0)
        cum = cv2.VideoCapture("http://10.5.17.149:8080")
        success, frame = cum.read()

        while success:
            ret, frame = cum.read()
            if not ret:
                break

            result = self.predict(frame)
            classes_names, classes, boxes = self.parse_result(result)
            command = ""

            local_name = None

            for box in result.boxes:
                for c in box.cls:
                    print(f'{classes_names[int(c)]} - 0')



            if local_name == None:
                pass
            elif local_name == "cube":
                command = "move-forward"
            elif local_name == "sphere":
                command = "stop"



            self.client_socket.send(command.encode('utf-8'))
            # raw_data = self.client_socket.recv(1024)
            # data = bytes(raw_data).decode('utf-8')
            # self.validate(data, command)

            # print(data)

            # NN

    def top_com(self):
        cum = cv2.VideoCapture("http://10.5.17.149:8080")
        success, frame = cum.read()

        while success:
            ret, frame = cum.read()
            if not ret:
                break

            result = self.predict(frame)
            classes_names, classes, boxes = self.parse_result(result)
            command = ""

            local_name = None

            for box in result.boxes:
                for c in box.cls:
                    print(f'{classes_names[int(c)]} - 1')


            if local_name == None:
                pass
            elif local_name == "cube":
                command = "move-forward"
            elif local_name == "sphere":
                command = "stop"




            self.client_socket.send(command.encode('utf-8'))
            # raw_data = self.client_socket.recv(1024)
            # data = bytes(raw_data).decode('utf-8')
            # self.validate(data, command)

            # print(data)


    def graph_run(self):
        pass


    def run(self) -> None:
        self.client_socket, address = self.socket.accept()

        Thread(target=self.down_cam, args=[]).start()
        Thread(target=self.top_com, args=[]).start()
        Thread(target=self.graph_run, args=[]).start()


cl = TcpServer()
cl.run()
