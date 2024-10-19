import socket

import fs_event as fs_ev
from fs_motor import FSMover
from fs_move_simple import Direction
from fs_movement import FsMovement


class FSocket:
    def __init__(self, fs_motor: FSMover, fs_movement: FsMovement):
        self.addr = ('192.168.2.121', 2002)
        self.fs_motor = fs_motor
        self.fs_movement = fs_movement
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect(self.addr)

    @fs_ev.bus.on('reconnect_tcp')
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
                fs_ev.bus.emit("reconnect_tcp", self)

    def resolve_command(self, command_string: str):
        if command_string == "stop":
            fs_ev.bus.emit("stop", self.fs_motor)
        if command_string == "move-forward":
            fs_ev.bus.emit("move", self.fs_motor, Direction.RIGHT)
        if command_string == "first_move":
            fs_ev.bus.emit('first_move', self.fs_movement, self.fs_motor)
