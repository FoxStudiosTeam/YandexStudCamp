import time

from fs_move_simple import create_graph, AStarPath
from fs_event import bus
from fs_motor import FSMover


def first_step(fs_motor: FSMover):
    nodes = create_graph()
    a_star_path = AStarPath(nodes)
    path = a_star_path.a_star_simple(nodes[0], nodes[208])
    for elem in path:
        bus.emit("move", fs_motor, elem.direction)
        time.sleep(1)
    bus.emit("stop",fs_motor)