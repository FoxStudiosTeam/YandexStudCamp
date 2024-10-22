import socket


class FSocket:
    def __init__(self):
        self.addr = ('192.168.1.236', 2002)
        # self.addr = ('127.0.0.1', 2002)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect(self.addr)

    def reconnect(self):
        self.client_socket.connect(self.addr)

    def run(self):
        self.connect()
        while True:
            try:
                command: bytes = self.client_socket.recv(1024)
                command_string = command.decode('utf-8')
                try:
                    self.resolve_command(command_string)

                except Exception as err:
                    print(err)
                    self.client_socket.send("error".encode('utf-8'))

            except Exception as e:
                print(e)
                self.reconnect()

    def resolve_command(self, command_string: str):
        commands = command_string.split('.')

        if commands[0] == "stop":
            print(f"received: {commands[0]}")
        if commands[0] == "move":
            print(f"received: {commands[0]} : {commands[1]}")
        if commands[0] == "color":
            print(f"received: {commands[0]} : {commands[1]}")
        if commands[0] == "catch_cube":
            print(f"received: {commands[0]} : catch_cube")
        if commands[0] == "catch_circle":
            print(f"received: {commands[0]} : catch_circle")
        if commands[0] == "push":
            print(f"received: {commands[0]} : push")
        if commands[0] == "drop":
            print(f"received: {commands[0]} : drop")
        if commands[0] == "normal_state":
            print(f"received: {commands[0]} : normal_state")
        if len(commands) > 1:
            if commands[0] == "aim" and commands[1] == "FORWARD":
                print(f"received: {commands[0]} : {commands[1]} : Direction.FORWARD")
            if commands[0] == "aim" and commands[1] == "RIGHT":
                print(f"received: {commands[0]} : {commands[1]} : Direction.RIGHT")
            if commands[0] == "aim" and commands[1] == "LEFT":
                print(f"received: {commands[0]} : {commands[1]} : Direction.LEFT")
            if commands[0] == "aim" and commands[1] == "BACK":
                print(f"received: {commands[0]} : {commands[1]} : Direction.BACK")
        if commands[0] == "check_wall":
            command = f"{True}"
            self.client_socket.send(command.encode('utf-8'))

fs = FSocket()
fs.run()