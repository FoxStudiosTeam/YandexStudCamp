import socket
import cv2


class TcpServer:
    def __init__(self):
        self.client_socket = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", 2002))
        self.socket.listen(1)

    def validate(self, message, command):
        if message == "error":
            self.client_socket.send(command.encode())
        if message == "ok":
            pass

    def test_fun(self) -> None:
        # cum = cv2.VideoCapture(f"{address[0]}:{address[1]}?action=stream")
        cum = cv2.VideoCapture(f"http://192.168.2.81:8080/?action=stream")
        success, frame = cum.read()

        while success:
            ret, frame = cum.read()

            cv2.imshow("pivo", frame)
            print("test")
            # NN
            command = "first_move"  # result of get->nn->result (multiple instances)
            self.client_socket.send(command.encode('utf-8'))
            raw_data = self.client_socket.recv(1024)
            data = bytes(raw_data).decode('utf-8')
            self.validate(data, command)

            print(data)

    def run(self) -> None:
        while True:
            # accept connections from outside
            self.client_socket, address = self.socket.accept()
            # now do something with the clientsocket
            # in this case, we'll pretend this is a threaded server

            # ct = client_thread(client_socket, address)
            self.test_fun()

            # received_data : bytes = self.client_socket.recv(1024)
            # print(received_data.decode())


cl = TcpServer()
cl.run()
