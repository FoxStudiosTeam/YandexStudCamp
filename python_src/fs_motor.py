import time

from fs_movement import Direction
import xr_config as cfg
from xr_motor import RobotDirection


class FSMover(RobotDirection):

    def stop(self):
        self.stop()

    def move(self, direction: Direction, last_direction: Direction):
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