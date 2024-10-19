from fs_move_simple import Direction
import fs_event as fs_ev
import time
import math

from xr_motor import RobotDirection

class FSMover(RobotDirection):

    cur_direction : Direction = None

    sec_t = 0.44

    sec_f = 1.25
    speed = 50/sec_f
    sec_d = speed/math.sqrt(2*(50**2))

    @fs_ev.bus.on('stop')
    def stop(self):
        super().stop()

    @fs_ev.bus.on('move')
    def move(self, next_direction : Direction):
        if self.cur_direction == None:
            self.cur_direction = Direction.FORWARD
        if next_direction == None:
            super().stop()
            return
        diff = next_direction.value - self.cur_direction.value
        if diff != 0:
            super().stop()
            if diff < 0:
                super().left()
                time.sleep(abs(diff//45)*self.sec_t)
                super().stop()
                self.cur_direction = next_direction
            elif diff > 0:
                super().right()
                time.sleep((diff//45)*self.sec_t)
                super().stop()
                self.cur_direction = next_direction
        if self.cur_direction == next_direction:
            super().forward()
            if self.cur_direction.value in [45, 135, 225, 315]:
                time.sleep(self.sec_d)
            elif self.cur_direction.value in [0, 90, 180, 270]: time.sleep(self.sec_f)
    @fs_ev.bus.on('go-back')
    def go_back(self, sec):
        super().back()
        time.sleep(sec)