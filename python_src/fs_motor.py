from fs_move_simple import Direction
from fs_event import bus

from xr_motor import RobotDirection

class FSMover(RobotDirection):

    @bus.on('stop')
    def stop(self):
        self.stop()

    @bus.on('move')
    def move(self, direction: Direction):
        if direction == Direction.FORWARD:
            self.forward()
        if direction == Direction.FORWARD_LEFT:
            self.stop()
        if direction == Direction.FORWARD_RIGHT:
            self.stop()
        if direction == Direction.RIGHT:
            self.right()
        if direction == Direction.LEFT:
            self.left()
        if direction == Direction.BACK:
            self.back()
        if direction == Direction.BACK_LEFT:
            self.stop()
        if direction == Direction.BACK_RIGHT:
            self.stop()

