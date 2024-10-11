import math
from queue import PriorityQueue
from enum import Enum


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
    def __init__(self, parent, x, y, is_block):
        self.x = x
        self.y = y
        self.parent = parent
        self.is_block = is_block,
        self.g_cost = 0,
        self.h_cost = 0,
        self.f_cost = 0

    def re_calc_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost


class AStarPath():
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def distance(self, from_point: Node, target_point: Node):
        return math.sqrt(math.pow((target_point.x - from_point), 2) + math.pow((target_point.y - from_point.y), 2))

    def get_neighbors(self, start_node: Node, node: Node, end_node: Node):
        neighbors = []

        for local_node in self.nodes:
            local_node.g_cost = self.distance(local_node, start_node)
            local_node.h_cost = self.distance(local_node, end_node)
            local_node.f_cost = local_node.g_cost + local_node.h_cost

            if ((local_node.x == node.x + 1) or (local_node.x == node.x - 1) or (local_node.y == node.y + 1) or (
                    local_node.y == node.y - 1)) and local_node.is_block != True:
                neighbors.append(local_node)

        return neighbors

    def a_star_simple(self, start_node: Node, end_node: Node, nodes: list[Node]):
        queue = PriorityQueue()
        queue.put((0, start_node))
        is_end = False
        current_node = start_node

        while is_end:
            if current_node == end_node:
                queue.put(end_node)
                is_end = True

            if current_node.is_block:
                continue

            neighbors = self.get_neighbors(start_node, current_node, end_node)

            minimal: Node = None
            i = 0
            for neighbor in neighbors:
                if i == 0:
                    minimal = neighbor

                if neighbor.f_cost < minimal.f_cost:
                    minimal = neighbor
                i += 1

            current_node = minimal
        return queue


def create_graph():
    nodes = []
    for x in range(8):
        for y in range(6):
            local_node = Node(None, x, y, False)
            nodes.append(local_node)

    return nodes


def test_graph():
    nodes = create_graph()
    a_star_path = AStarPath(nodes)
    # a_star_path.a_star_simple(nodes[0], nodes[4],nodes)


test_graph()
