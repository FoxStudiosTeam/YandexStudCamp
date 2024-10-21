import socket

import fs_event as fs_ev
from fs_motor import FSMover
from fs_move_simple import Direction
from fs_movement import FsMovement
from fs_move_hand import Hand


class FSocket:
    def __init__(self, fs_motor: FSMover, fs_movement: FsMovement, fs_hand: Hand):
        self.addr = ('192.168.2.121', 2002)
        self.fs_motor = fs_motor
        self.fs_movement = fs_movement
        self.fs_hand = fs_hand
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
        commands = command_string.split('.')

        if commands[0] == "stop":
            fs_ev.bus.emit("stop", self.fs_motor)
        if commands[0] == "move":
            fs_ev.bus.emit("move", self.fs_motor, Direction.__getitem__(commands[1]))
        if commands[0] == "color":
            fs_ev.bus.emit("color", commands[1])
        if commands[0] == "aim.FORWARD":
            fs_ev.bus.emit("aim", self.fs_motor, Direction.FORWARD)
        if commands[0] == "aim.RIGHT":
            fs_ev.bus.emit("aim", self.fs_motor, Direction.RIGHT)
        if commands[0] == "aim.LEFT":
            fs_ev.bus.emit("aim", self.fs_motor, Direction.LEFT)
        if commands[0] == "aim.BACK":
            fs_ev.bus.emit("aim", self.fs_motor, Direction.BACK)
        if commands[0] == "catch_cube":
            fs_ev.bus.emit("catch_cube", self.fs_hand)
        if commands[0] == "catch_circle":
            fs_ev.bus.emit("catch_circle", self.fs_hand)
        if commands[0] == "push":
            fs_ev.bus.emit("push", self.fs_hand)
        if commands[0] == "drop":
            fs_ev.bus.emit("drop", self.fs_hand)
        if commands[0] == "normal_state":
            fs_ev.bus.emit("normal_state", self.fs_hand)
        