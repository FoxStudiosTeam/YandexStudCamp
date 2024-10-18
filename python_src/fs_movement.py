import time

from fs_move_simple import create_graph, AStarPath, Direction
import fs_event as fs_ev
from fs_motor import FSMover



class FsMovement:
    @fs_ev.bus.on('first_move')
    def first_step(self, fs_motor: FSMover):
        a_star_path = AStarPath()
        nodes = create_graph()
        path = a_star_path.a_star_simple(nodes[0], nodes[208], nodes)
        for elem in path:
            fs_ev.bus.emit("move", fs_motor, elem.direction)
            time.sleep(1)
        fs_ev.bus.emit("stop", fs_motor)

    @fs_ev.bus.on('metering_test')
    def test_metering(self, fs_motor : FSMover, sec : int = 1, direction : Direction = Direction.FORWARD):
        fs_ev.bus.emit("move",fs_motor, direction)
        time.sleep(sec)
        fs_ev.bus.emit("stop", fs_motor)

