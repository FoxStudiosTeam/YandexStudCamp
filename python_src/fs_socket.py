import socket
import fs_event as fs_ev
from fs_motor import FSMover
from fs_move_simple import Direction
from xr_startmain import fs_motor


class FSocket:
    def __init__(self,fs_motor : FSMover):
        self.addr = ('192.168.2.121', 2002)
        self.fs_motor = fs_motor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect(self.addr)

    @fs_ev.bus.on('reconnect_tcp')
    def reconnect(self):
        self.client_socket.connect(self.addr)

    def run(self):
        while True:
            try:
                command = self.client_socket.recv(1024)
                command_string = bytes(command).decode('utf-8')
                self.resolve_command(command_string)
            except Exception as e:
                print(e)
                fs_ev.bus.emit("reconnect_tcp",self)

    def resolve_command(self, command_string: str):
        if command_string == "stop":
            fs_ev.bus.emit("stop",fs_motor)
        if command_string == "move-forward":
            fs_ev.bus.emit("move",fs_motor, Direction.FORWARD)