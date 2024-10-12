import math
from queue import PriorityQueue

class Node:
    def __init__(self, parent : object, x, y, is_block):
        self.x = x
        self.y = y
        self.parent = None
        self.is_block = is_block
        self.g_cost: float = 0
        self.h_cost: float = 0
        self.f_cost: float = 0

    def re_calc_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost


class AStarPath():
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def distance(self, from_point: Node, target_point: Node):
        return math.sqrt(math.pow((target_point.x - from_point.x), 2) + math.pow((target_point.y - from_point.y), 2))

    def get_neighbors(self, node: Node, end_node: Node):
        neighbors = []

        for local_node in self.nodes:
            if local_node == end_node:
                local_node.f_cost = 0

            local_node.h_cost = self.distance(local_node, end_node)
            local_node.f_cost = local_node.g_cost + local_node.h_cost

            if (((local_node.x == node.x + 1) or (local_node.x == node.x - 1)) and 
                ((local_node.y == node.y + 1) or (local_node.y == node.y - 1))) and local_node != node:
                neighbors.append(local_node)
            elif (((local_node.x == node.x) and ((local_node.y == node.y + 1) or (local_node.y == node.y - 1))) or 
                ((local_node.y == node.y) and ((local_node.x == node.x + 1) or (local_node.x == node.x - 1)))) and local_node != node:
                neighbors.append(local_node)

        return neighbors


    def a_star_simple(self, start_node: Node, end_node: Node, nodes: list[Node]):
        queue = PriorityQueue()
        queue.put((0, start_node))
        current_node = start_node
        recent : list[Node] = []
        j = 1
        
        while True:
            if current_node == end_node:
                return queue
            
            neighbors = self.get_neighbors(current_node, end_node)

            if current_node.is_block == True:
                current_node = recent[len(recent)-1]
                continue

            minimal: Node = None
            i = 0

            for neighbor in neighbors:
                if i == 0 and neighbor.is_block == False and neighbor not in recent:
                    minimal = neighbor
                elif i == 0:
                    continue
                if (neighbor.f_cost+j < minimal.f_cost+j) and (neighbor not in recent) and neighbor.is_block == False:
                    minimal = neighbor
                else:
                    recent.append(neighbor)
                i += 1

            j += 1
            queue.put((j, minimal))
            recent.append(current_node)
            current_node = minimal


def create_graph():
    nodes = []
    modifier = 4
    for x in range(8*modifier):
        for y in range(6*modifier):
            if ((((x >= 7 and x <= 12) or (x >= 19 and x <= 24))  and y == 3) or (x == 7 and ((y >= 3 and y <= 8) or (y >= 15 and y <= 20))) or (y == 20 and ((x >= 7 and x <= 12) or (x >= 19 and x <= 24))) or (x == 24 and ((y >= 3 and y <= 8) or (y >= 15 and y <= 20)))):
                nodes.append(Node(None, x, y, True))
            else:
                local_node = Node(None, x, y, False)
                nodes.append(local_node)

    return nodes


def test_graph():
    nodes = create_graph()
    a_star_path = AStarPath(nodes)
    return a_star_path.a_star_simple(nodes[0], nodes[0], nodes)
