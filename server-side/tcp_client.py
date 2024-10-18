import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("127.0.0.1",2002))

while True:
    try:
        client_socket.send(bytes("test",encoding="utf-8"))
        data = client_socket.recv(1024)
        print(f"Received {data}")

    except Exception as e:
        time.sleep(10)
        client_socket.connect(("127.0.0.1",2002))