import math
from enum import Enum
from queue import PriorityQueue
from typing import List


class Direction(Enum):
    FORWARD = 1
    FORWARD_LEFT = 2
    FORWARD_RIGHT = 3
    LEFT = 4
    RIGHT = 5
    BACK = 6
    BACK_LEFT = 7
    BACK_RIGHT = 8


class Node:
    def __init__(self, parent : object, x : int, y : int, is_block : bool):
        self.direction = None
        self.x = x
        self.y = y
        self.parent = None
        self.is_block = is_block
        self.g_cost: float = 0
        self.h_cost: float = 0
        self.f_cost: float = 0

    def re_calc_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost  # Define how to compare nodes based on f_cost

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y  # Define equality based on coordinates


class NodeUtil:
    '''
    Направление относительно сетки координат, которую строит граф:
    [00] [10] [20]
    [01] [11] [21]
    [02] [12] [22]
    FORWARD - вверх
    BACK - вниз
    '''
    def validate_direction(self, cur_node : Node, next_node : Node) -> Direction:
        dir_x = next_node.x - cur_node.x
        dir_y = next_node.y - cur_node.y
        if dir_x == 0 and dir_y < 0: return Direction.FORWARD
        if dir_x == 0 and dir_y > 0: return Direction.BACK
        if dir_x < 0 and dir_y > 0: return Direction.BACK_LEFT
        if dir_x > 0 and dir_y > 0: return Direction.BACK_RIGHT
        if dir_x < 0 and dir_y < 0: return Direction.FORWARD_LEFT
        if dir_x > 0 and dir_y < 0: return Direction.FORWARD_RIGHT
        if dir_x < 0 and dir_y == 0: return Direction.LEFT
        if dir_x > 0 and dir_y == 0: return Direction.RIGHT



class AStarPath:
    def distance(self, from_point: Node, target_point: Node):
        return math.sqrt(math.pow((target_point.x - from_point.x), 2) + math.pow((target_point.y - from_point.y), 2))

    def get_neighbors(self, node: Node, end_node: Node,nodes: List[Node]):
        neighbors = []

        node_util = NodeUtil()

        for local_node in nodes:
            if local_node == end_node:
                local_node.f_cost = 0

            local_node.h_cost = self.distance(local_node, end_node)
            local_node.f_cost = local_node.g_cost + local_node.h_cost

            local_node.direction = node_util.validate_direction(node, local_node)

            if (((local_node.x == node.x + 1) or (local_node.x == node.x - 1)) and
                ((local_node.y == node.y + 1) or (local_node.y == node.y - 1))) and local_node != node:
                neighbors.append(local_node)
            elif (((local_node.x == node.x) and ((local_node.y == node.y + 1) or (local_node.y == node.y - 1))) or
                ((local_node.y == node.y) and ((local_node.x == node.x + 1) or (local_node.x == node.x - 1)))) and local_node != node:
                neighbors.append(local_node)

        return neighbors


    # def a_star_simple(self, start_node: Node, end_node: Node, nodes: List[Node]) -> list[Node]:
    #     queue = PriorityQueue()
    #     queue.put((0, start_node))
    #     current_node = start_node
    #     recent : list[Node] = []
    #     j = 1
    #
    #     while True:
    #         if current_node == end_node:
    #             return queue
    #
    #         neighbors = self.get_neighbors(current_node, end_node)
    #
    #         if current_node.is_block == True:
    #             current_node = recent[len(recent)-1]
    #             continue
    #
    #         minimal: Node = None
    #         i = 0
    #
    #         for neighbor in neighbors:
    #             if i == 0 and neighbor.is_block == False and neighbor not in recent:
    #                 minimal = neighbor
    #             elif i == 0:
    #                 continue
    #             if (neighbor.f_cost+j < minimal.f_cost+j) and (neighbor not in recent) and neighbor.is_block == False:
    #                 minimal = neighbor
    #             else:
    #                 recent.append(neighbor)
    #             i += 1
    #
    #         j += 1
    #         queue.put((j, minimal))
    #         recent.append(current_node)
    #         current_node = minimal

    from queue import PriorityQueue

    def a_star_simple(self, start_node: Node, end_node: Node,nodes: List[Node]) -> List[Node]:
        queue = PriorityQueue()
        queue.put((0, start_node))
        start_node.g_cost = 0
        recent = []

        while not queue.empty():
            current_node = queue.get()[1]

            if current_node == end_node:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent
                path.reverse()
                return path

            if current_node.is_block:
                continue

            recent.append(current_node)

            neighbors = self.get_neighbors(current_node, end_node,nodes)

            for neighbor in neighbors:
                if neighbor.is_block or neighbor in recent:
                    continue

                tentative_g_cost = current_node.g_cost + self.distance(current_node, neighbor)

                if tentative_g_cost < neighbor.g_cost or neighbor not in [n[1] for n in queue.queue]:
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = self.distance(neighbor, end_node)
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent = current_node
                    queue.put((neighbor.f_cost, neighbor))

        return []


def create_graph():
    nodes = []
    modifier = 4
    for x in range(8*modifier):
        for y in range(6*modifier):
            if ((((x >= 7 and x <= 12) or (x >= 19 and x <= 24))  and y == 3) or (x == 7 and ((y >= 3 and y <= 8) or (y >= 15 and y <= 20))) or (y == 20 and ((x >= 7 and x <= 12) or (x >= 19 and x <= 24))) or (x == 24 and ((y >= 3 and y <= 8) or (y >= 15 and y <= 20)))):
            #if x == 12 and y > 1:
                nodes.append(Node(None, x, y, True))
            else:
                local_node = Node(None, x, y, False)
                nodes.append(local_node)

    return nodes


def test_graph():
    nodes = create_graph()
    a_star_path = AStarPath(nodes)
    return a_star_path.a_star_simple(nodes[0], nodes[0], nodes)
