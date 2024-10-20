import time

from fs_move_simple import Direction
import fs_event as fs_ev
from fs_motor import FSMover


class FsMovement:

    @fs_ev.bus.on('move_forward')
    def move_forward(self,fs_motor : FSMover, direction : Direction):
        fs_ev.bus.emit("move",fs_motor, direction)
        fs_ev.bus.emit("stop", fs_motor)


    @fs_ev.bus.on('metering_test')
    def test_metering(self, fs_motor : FSMover, direction : Direction = Direction.FORWARD):
        fs_ev.bus.emit("move",fs_motor, direction)
        fs_ev.bus.emit("stop", fs_motor)

fs_motor = FSMover()
fs_movement = FsMovement()

def test(direction : Direction = Direction.FORWARD):
    fs_ev.bus.emit('metering_test', fs_movement, fs_motor, direction)