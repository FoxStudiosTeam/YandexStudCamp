import socket
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

        self.model = YOLO("./best.pt")
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

    def test_fun(self) -> None:
        # cum = cv2.VideoCapture(f"{address[0]}:{address[1]}?action=stream")
        cum = cv2.VideoCapture(f"http://192.168.2.81:8080/?action=stream")
        success, frame = cum.read()

        while success:
            ret, frame = cum.read()
            if not ret:
                break

            result = self.predict(frame)
            classes_names, classes, boxes = self.parse_result(result)
            command = ""

            if len(boxes) == 0:
                command = "stop"  # result of get->nn->result (multiple instances)
            else:
                command = "move-forward"  # result of get->nn->result (multiple instances)

            self.client_socket.send(command.encode('utf-8'))
            # raw_data = self.client_socket.recv(1024)
            # data = bytes(raw_data).decode('utf-8')
            # self.validate(data, command)

            # print(data)
            cv2.imshow("pivo", frame)
            print("test")
            break
            # NN

    def run(self) -> None:
        self.client_socket, address = self.socket.accept()

        while True:
            print("a")
            # accept connections from outside
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server

            # ct = client_thread(client_socket, address)
            self.test_fun()

            # received_data : bytes = self.client_socket.recv(1024)
            # print(received_data.decode())


cl = TcpServer()
cl.run()
