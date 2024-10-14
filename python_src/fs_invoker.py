import time

import fs_event as fs_ev
from fs_move_simple import Direction


def test():
    fs_ev.bus.emit('move', Direction.FORWARD)
    time.sleep(2)
    fs_ev.bus.emit('stop')