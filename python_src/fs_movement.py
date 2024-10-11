from fs_move_simple import *


nodes = create_graph()


class Direction(Enum):
    FORWARD = 1
    FORWARD_LEFT = 2
    FORWARD_RIGHT = 3
    LEFT = 4
    RIGHT = 5
    BACK = 6
    BACK_LEFT = 7
    BACK_RIGHT = 8


class Determining():
    def __init__(self, cur_node : Node, next_node : Node):
        dir_x = cur_node.x - next_node.x
        dir_y = cur_node.y - next_node.y
        if dir_x > 0 and dir_y > 0: return Direction.FORWARD_LEFT
        if dir_x > 0 and dir_y < 0: return Direction.BACK_LEFT
        if dir_x < 0 and dir_y > 0: return Direction.FORWARD_RIGHT
        if dir_x < 0 and dir_y < 0: return Direction.BACK_RIGHT
        if dir_x == 0 and dir_y > 1: return Direction.BACK