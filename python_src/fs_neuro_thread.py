import time

import fs_event as fs_ev
from fs_top_camera_utils import TopCameraUtils
from fs_motor import FSMover

class NeuroThread:
    def __init__(self, mover: FSMover):
        self.cameraUtils = TopCameraUtils(400,310)
        self.mover = mover

    def stop_event(self):
        fs_ev.bus.emit('stop',self.mover)



    def run(self):

       while True:
           #init - neural-network
           x,y = self.cameraUtils.calculate_current_pos((10,20))
           print(x,y)
           self.stop_event()
           time.sleep(1)