import time

import fs_event as fs_ev

from fs_move_simple import Direction
from fs_motor import FSMover


def test(fs_motor: FSMover):
    fs_ev.bus.emit('move', fs_motor,Direction.FORWARD)
    time.sleep(2)
    fs_ev.bus.emit('stop')