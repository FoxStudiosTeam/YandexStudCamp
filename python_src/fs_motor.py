from fs_move_simple import Direction
import fs_event as fs_ev
import time
import math

from xr_motor import RobotDirection

class FSMover(RobotDirection):

    cur_direction : Direction = None

    sec_tr = 0.337
    sec_tl = 0.353
    sec_tar = 0.33

    sec_f = 0.327
    speed = 12.2/sec_f
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
        if diff > 180: diff -= 360
        elif diff < -180: diff += 360
        if diff != 0:
            super().stop()
            if diff == 180 or diff == -180:
                super().right()
                time.sleep(4*self.sec_tar)
                super().stop()
                time.sleep(0.1)
                self.cur_direction = next_direction
            elif diff == 45:
                super().right()
                time.sleep(self.sec_tr)
                super().stop()
                time.sleep(0.1)
                self.cur_direction = next_direction
            elif diff == -45:
                super().left()
                time.sleep(self.sec_tl)
                super().stop()
                time.sleep(0.1)
                self.cur_direction = next_direction
            elif diff == 90:
                super().right()
                time.sleep(2*self.sec_tr)
                super().stop()
                time.sleep(0.1)
                self.cur_direction = next_direction
            elif diff == -90:
                super().left()
                time.sleep(2*self.sec_tl)
                super().stop()
                time.sleep(0.1)
                self.cur_direction = next_direction
            elif diff == 135:
                super().right()
                time.sleep(3*self.sec_tar)
                super().stop()
                time.sleep(0.1)
                self.cur_direction = next_direction
            elif diff == -135:
                super().left()
                time.sleep(2*self.sec_tl)
                super().stop()
                time.sleep(0.1)
                self.cur_direction = next_direction
        if self.cur_direction == next_direction:
            super().forward()
            if self.cur_direction.value in [45, 135, 225, 315]: time.sleep(self.sec_d)
            elif self.cur_direction.value in [0, 90, 180, 270]: time.sleep(self.sec_f)
            super().stop()
        
    @fs_ev.bus.on('go-back')
    def go_back(self):
        super().back()
        time.sleep(self.sec_f)
        super().stop()

    @fs_ev.bus.on('aim')
    def aim(self,direction: Direction):
        if direction.name == 'RIGHT':
            super().right()
            time.sleep(0.1)
            super().stop()
            time.sleep(0.1)
        elif direction.name == 'LEFT':
            super().left()
            time.sleep(0.1*(self.sec_tr/self.sec_tl))
            super().stop()
            time.sleep(0.1)
        elif direction.name == 'FORWARD':
            super().forward()
            time.sleep(0.1)
            super().stop()
            time.sleep(0.1)
        elif direction.name == 'BACK':
            super().back()
            time.sleep(0.1)
            super().stop()
            time.sleep(0.1)