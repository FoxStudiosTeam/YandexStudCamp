import socket
from threading import Thread
from typing import Tuple
from event_bus import EventBus

import cv2


bus = EventBus()

def resolve_message(message:str,command:str,socket:socket):
    if message == "error":
        send(command,socket)
    if message == "ok":
        pass


def send(message:str,socket:socket):
    socket.send(bytes(message, encoding="utf-8"))

def test_fun(socket:socket,address:Tuple[str,int]) -> None:
    # cum = cv2.VideoCapture(f"{address[0]}:{address[1]}?action=stream")
    cum = cv2.VideoCapture(f"http://192.168.2.81:8080/?action=stream")
    success, frame = cum.read()
    while success:
        ret, frame = cum.read()
        if not ret:
            cv2.imshow("pivo",frame)


            #NN
            command = "move-forward" #result of get->nn->result (multiple instances)
            socket.send(bytes(command, encoding="utf-8"))
            raw_data = socket.recv(1024)
            data = bytes(raw_data).decode('utf-8')
            resolve_message(data,command,socket)


            #socket.send(bytes("stop", encoding="utf-8"))




def client_thread(socket:socket,address:Tuple[str,int]) -> Thread:
    #print(socket.client)
    print(socket)
    print(address)
    return Thread(test_fun(socket,socket))


# create an INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
server_socket.bind(("0.0.0.0", 2002))
# become a server socket
server_socket.listen(1)

while True:
    # accept connections from outside
    client_socket, address = server_socket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server

    ct = client_thread(client_socket,address)
    received_data = client_socket.recv(1024)

    b = f"test-message, received: {received_data}"
    client_socket.sendall(bytes(b,encoding="utf-8"))

    ct.run()

