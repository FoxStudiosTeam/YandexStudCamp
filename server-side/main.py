import socket
from threading import Thread

import cv2


def test_fun(socket,address:str):
    cum = cv2.VideoCapture(address)
    while cum.isOpened():
        ret, frame = cum.read()
        if not ret:
            cv2.imshow("pivo",frame)


def client_thread(socket:socket,address:str) -> Thread:
    print(socket.client)
    return Thread(test_fun(socket))


# create an INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
server_socket.bind(("0.0.0.0", 2002))
# become a server socket
server_socket.listen(1)

while True:
    # accept connections from outside
    (clientsocket, address) = server_socket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket,address)
    ct.run()

