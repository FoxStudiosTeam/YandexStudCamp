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
        self.is_block = is_block



class AStarPath():
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def get_neighbors(self, node: Node):
        neighbors = []

        for local_node in self.nodes:
            if (local_node.x == node.x + 1) or (local_node.x == node.x - 1) or (local_node.y == node.y + 1) or (
                    local_node.y == node.y - 1):
                neighbors.append(local_node)

        return neighbors

    # def a_star_simple(self, start_node: Node, end_node: Node, nodes: list[Node]):
    #     queue = PriorityQueue()
    #     queue.put(start_node)
    #     is_end = False
    #     current_node = start_node
    #     while is_end:
    #         if current_node == end_node:
    #             queue.put(end_node)
    #             is_end = True
    #
    #         if current_node.is_block:
    #             continue
    #
    #         neighbors = self.get_neighbors(current_node)
    #
    #         for neighbor in neighbors:





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