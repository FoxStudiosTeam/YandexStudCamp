from fs_move_simple import Direction
import fs_event as fs_ev

from xr_motor import RobotDirection

class FSMover(RobotDirection):

    @fs_ev.bus.on('stop')
    def stop(self):
        super().stop()

    @fs_ev.bus.on('move')
    def move(self, direction: Direction):
        if direction == Direction.FORWARD:
            super().forward()
        if direction == Direction.FORWARD_LEFT:
            super().stop()
        if direction == Direction.FORWARD_RIGHT:
            super().stop()
        if direction == Direction.RIGHT:
            super().right()
        if direction == Direction.LEFT:
            super().left()
        if direction == Direction.BACK:
            super().back()
        if direction == Direction.BACK_LEFT:
            super().stop()
        if direction == Direction.BACK_RIGHT:
            super().stop()

