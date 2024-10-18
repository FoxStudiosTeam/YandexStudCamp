from fs_move_simple import Direction
import fs_event as fs_ev
import time

from xr_motor import RobotDirection

class FSMover(RobotDirection):

    @fs_ev.bus.on('stop')
    def stop(self):
        super().stop()

    @fs_ev.bus.on('move')
    def move(self, cur_direction : Direction, next_direction : Direction):
        diff = next_direction.value - cur_direction.value
        if diff != 0:
            super().stop()
            if diff < 0:
                super().left()
                time.sleep(abs(diff//45))
                super().stop()
                cur_direction = next_direction
            elif diff > 0:
                super().right()
                time.sleep(diff//45)
                super().stop()
                cur_direction = next_direction
        if cur_direction == next_direction:
            super().forward()
            if cur_direction in [45, 135, 225, 315]:
                time.sleep(1.76)
            elif cur_direction in [0, 90, 180, 270]: time.sleep(1.25)
    @fs_ev.bus.on('go-back')
    def go_back(self, sec):
        super().back()
        time.sleep(sec)