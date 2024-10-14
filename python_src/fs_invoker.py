import time

import fs_event as fs_ev
from xr_startmain import fs_motor

from fs_move_simple import Direction


def test():
    fs_ev.bus.emit('move', fs_motor,Direction.FORWARD)
    time.sleep(2)
    fs_ev.bus.emit('stop')