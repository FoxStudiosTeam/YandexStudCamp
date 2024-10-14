import time

from fs_event import bus
from fs_move_simple import Direction


def test():
    bus.emit('move', Direction.FORWARD)
    time.sleep(2)
    bus.emit('stop')