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
    '''
    Направление относительно сетки координат, которую строит граф:
    [00] [10] [20]
    [01] [11] [21]
    [02] [12] [22]
    FORWARD - вверх
    BACK - вниз
    '''
    def __init__(self, cur_node : Node, next_node : Node):
        dir_x = next_node.x - cur_node.x
        dir_y = next_node.y - cur_node.y
        if dir_x > 0 and dir_y > 0: return Direction.BACK_RIGHT
        if dir_x > 0 and dir_y < 0: return Direction.FORWARD_RIGHT
        if dir_x < 0 and dir_y > 0: return Direction.BACK_LEFT
        if dir_x < 0 and dir_y < 0: return Direction.FORWARD_LEFT
        if dir_x == 0 and dir_y > 0: return Direction.BACK
        if dir_x == 0 and dir_y < 0: return Direction.FORWARD
        if dir_x > 0 and dir_y == 0: return Direction.RIGHT
        if dir_x < 0 and dir_y == 0: return Direction.LEFT