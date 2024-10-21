import socket
import time
from enum import Enum
from queue import PriorityQueue
from threading import Thread
from typing import List, Tuple
from fs_top_camera_utils import TopCameraUtils

import cv2
import math
import numpy as np
from ultralytics import YOLO


class Direction(Enum):
    FORWARD = 0
    FORWARD_LEFT = 315
    FORWARD_RIGHT = 45
    LEFT = 270
    RIGHT = 90
    BACK = 180
    BACK_LEFT = 225
    BACK_RIGHT = 135


class Node:
    def __init__(self, parent: object, x: int, y: int, is_block: bool):
        self.direction_grad: int = 0
        self.direction: Direction = None
        self.x = x
        self.y = y
        self.parent: Node = None
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

    def validate_direction(self, cur_node: Node, next_node: Node) -> Tuple[Direction, int]:
        dir_x = next_node.x - cur_node.x
        dir_y = next_node.y - cur_node.y
        if dir_x == 0 and dir_y < 0: return Direction.FORWARD, 0
        if dir_x == 0 and dir_y > 0: return Direction.BACK, 180
        if dir_x < 0 and dir_y > 0: return Direction.BACK_LEFT, 225
        if dir_x > 0 and dir_y > 0: return Direction.BACK_RIGHT, 135
        if dir_x < 0 and dir_y < 0: return Direction.FORWARD_LEFT, 315
        if dir_x > 0 and dir_y < 0: return Direction.FORWARD_RIGHT, 45
        if dir_x < 0 and dir_y == 0: return Direction.LEFT, 270
        if dir_x > 0 and dir_y == 0: return Direction.RIGHT, 90

    def create_graph(self):
        nodes = []
        modifier = 4
        for x in range(8 * modifier):
            for y in range(6 * modifier):
                if ((((x >= 7 and x <= 13) or (x >= 18 and x <= 24)) and y == 3) or
                        (((x >= 7 and x <= 13) or (x >= 18 and x <= 24)) and y == 4) or
                        (((y >= 3 and y <= 9) or (y >= 14 and y <= 20)) and x == 7) or
                        (((y >= 3 and y <= 9) or (y >= 14 and y <= 20)) and x == 8) or
                        (((x >= 7 and x <= 13) or (x >= 18 and x <= 24)) and y == 20) or
                        (((x >= 7 and x <= 13) or (x >= 18 and x <= 24)) and y == 19) or
                        (((y >= 3 and y <= 9) or (y >= 14 and y <= 20)) and x == 24) or
                        (((y >= 3 and y <= 9) or (y >= 14 and y <= 20)) and x == 23) or
                        (((x == 12 or x == 13) or (x == 18 or x == 19)) and (
                                (y == 8 or y == 9) or (y == 15 or y == 14)))):
                    # if x == 12 and y > 1:
                    nodes.append(Node(None, x, y, True))
                else:
                    local_node = Node(None, x, y, False)
                    nodes.append(local_node)

        return nodes


class AStarPath:
    def distance(self, from_point: Node, target_point: Node):
        return math.sqrt(math.pow((target_point.x - from_point.x), 2) + math.pow((target_point.y - from_point.y), 2))

    def get_neighbors(self, node: Node, end_node: Node, nodes: List[Node]):
        neighbors: List[Node] = []

        for local_node in nodes:
            if local_node == end_node:
                local_node.f_cost = 0

            local_node.h_cost = self.distance(local_node, end_node)
            local_node.f_cost = local_node.g_cost + local_node.h_cost
            if (((local_node.x == node.x + 1) or (local_node.x == node.x - 1)) and
                ((local_node.y == node.y + 1) or (local_node.y == node.y - 1))) and local_node != node:
                neighbors.append(local_node)
            elif (((local_node.x == node.x) and ((local_node.y == node.y + 1) or (local_node.y == node.y - 1))) or
                  ((local_node.y == node.y) and (
                          (local_node.x == node.x + 1) or (local_node.x == node.x - 1)))) and local_node != node:
                neighbors.append(local_node)

        return neighbors

    def a_star_simple(self, start_node: Node, end_node: Node, nodes: List[Node]) -> List[Node]:
        queue = PriorityQueue()
        queue.put((0, start_node))
        start_node.g_cost = 0
        recent = []
        node_util = NodeUtil()

        while not queue.empty():
            current_node = queue.get()[1]

            if current_node == end_node:
                path = []
                while current_node:
                    path.append(current_node)
                    if current_node.parent:
                        current_node.parent.direction, current_node.parent.direction_grad = node_util.validate_direction(
                            current_node.parent, current_node)
                    current_node = current_node.parent
                path.reverse()
                return path

            if current_node.is_block:
                continue

            recent.append(current_node)

            neighbors = self.get_neighbors(current_node, end_node, nodes)

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


class Target(Enum):
    CIRCLE = 0
    CUBE = 1
    CART = 2
    BUTTON = 3
    BASE = 4


class TcpServer:
    def __init__(self):
        self.target_catched = False
        self.current_node = None
        self.target: Node = None
        self.client_socket = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", 2002))
        self.socket.listen(1)

        self.labels = [
            "circle",
            "box",
            # "int",
            # "geo",
            # "pro",
            # "non"
        ]

        self.colors = [
            (47, 70, 238),
            (148, 155, 255),
            (27, 106, 255),
            (20, 181, 252),
            (61, 206, 207),
        ]

        self.image_size = (1, 1)

        self.model = YOLO("./Artem_welll_01.pt")
        self.is_target_visible: bool = False
        self.a_star = AStarPath()
        self.current_graph: List[Node] = []
        self.current_path: List[Node] = []
        self.current_direction: Direction = None
        self.top_camera_utils = None
        self.last_target_name: Target = None
        self.target_name: Target = None
        self.next_target_name: Target = None
        self.node_util: NodeUtil = NodeUtil()
        self.is_path_suspended: bool = False

    def predict(self, frame):
        return self.model.predict(frame)[0]

    def validate(self, message, command):
        if message == "error":
            self.client_socket.send(command.encode())
        if message == "ok":
            pass

    def parse_result(self, data):
        classes_names = data.names
        classes = data.boxes.cls.cpu().numpy()
        boxes = data.boxes.xyxy.cpu().numpy().astype(np.int32)
        return classes_names, classes, boxes

    def is_target_inside(self, x_centered: int, y_centered: int) -> bool:
        # x01- левая граница захвата = 73
        # y01 - верхняя граница захвата = 193
        # х02 - правая граница = 276
        # у02 - нижняя граница = 237
        # внутри = x01 < x_centered < x02; y01 < y_centered < y02;


        if (73 < x_centered < 276) and (193 < y_centered < 237 ):
            return True
        else:
            return False

    def down_cam(self) -> None:
        # cum = cv2.VideoCapture(f"{address[0]}:{address[1]}?action=stream")
        # cum = cv2.VideoCapture(f"http://192.168.2.81:8080/?action=stream")
        # cum = cv2.VideoCapture(0)
        cum = cv2.VideoCapture("http://10.5.17.149:8080")
        success, frame = cum.read()

        while success:
            ret, frame = cum.read()
            if not ret:
                break

            result = self.predict(frame)
            classes_names, classes, boxes = self.parse_result(result)
            command = ""

            local_name = None

            for box in result.boxes:
                x0, y0, x1, y1 = box.xyxy.cpu().numpy().astype(np.int32)
                x_centered = x1 - x0
                y_centered = y1 - y0
                flag = self.is_target_inside(x_centered, y_centered)

                if self.is_path_suspended == True and self.target_catched == False:
                    if local_name == None:
                        command = f"move.{Direction.LEFT.name}"
                        self.client_socket.send(command.encode('utf-8'))
                        continue
                    elif (local_name == "cube" or local_name == "circle") and (self.target_name == Target.CUBE or self.target_name == Target.CIRCLE) and self.is_path_suspended == True:
                        command = f"move.{Direction.RIGHT.name}"


                        self.client_socket.send(command.encode('utf-8'))
                    elif local_name == "button" and self.target_name == Target.BUTTON and self.is_path_suspended == True:

                        self.client_socket.send(command.encode('utf-8'))
        # raw_data = self.client_socket.recv(1024)
        # data = bytes(raw_data).decode('utf-8')
        # self.validate(data, command)

        # print(data)

        # NN


    def top_cum(self):
        # cum = cv2.VideoCapture("http://10.5.17.149:8080")
        cum = cv2.VideoCapture(0)
        success, frame = cum.read()

        while success:
            ret, frame = cum.read()
            if not ret:
                break

            result = self.predict(frame)
            classes_names, classes, boxes = self.parse_result(result)
            command = ""

            if self.last_target_name == Target.CIRCLE or self.last_target_name == Target.CUBE:
                self.last_target_name = self.target_name
                self.target_name = Target.CART
            if self.last_target_name == Target.CART:
                self.last_target_name = self.target_name
                self.target_name = Target.BUTTON

            for box in result.boxes:
                for c in box.cls:
                    if c == "game-border":
                        x0, y0, x1, y1 = box.xyxy.cpu().numpy().astype(np.int32)
                        self.top_camera_utils = TopCameraUtils(x1 - x0, y1 - y0)

                    print(f'{classes_names[int(c)]} - 1')

                    if self.top_camera_utils != None:
                        cls_nm = classes_names[int(c)]

                        if cls_nm == self.target_name.name.lower():
                            x0, y0, x1, y1 = box.xyxy.cpu().numpy().astype(np.int32)
                            (x, y) = self.top_camera_utils.calculate_current_pos((x1 - x0, y1 - y0))

                            for elem in self.current_graph:
                                if elem.x == x and elem.y == y:
                                    self.target = elem
                                    break

            # raw_data = self.client_socket.recv(1024)
            # data = bytes(raw_data).decode('utf-8')
            # self.validate(data, command)

            # print(data)


    def graph_run(self) -> None:
        self.current_path = self.a_star.a_star_simple(self.current_node, self.target, self.current_graph)

        if self.is_path_suspended == False:
            for elem in self.current_path:
                self.current_node = elem

                if elem.is_block == True:
                    command = f"stop"
                    self.client_socket.send(command.encode('utf-8'))
                    self.last_target_name = self.target_name
                    self.current_path = self.a_star.a_star_simple(self.current_node, self.target, self.current_graph)
                    self.graph_run()

                if self.current_node == self.current_path[len(self.current_path) - 1]:
                    command = f"stop"
                    self.is_path_suspended = True
                    self.last_target_name = self.target_name
                    self.client_socket.send(command.encode('utf-8'))



                else:
                    command = f"move.{elem.direction.name}"
                    self.client_socket.send(command.encode('utf-8'))
                time.sleep(0.005)
        else:
            while self.is_path_suspended == True:
                print("suspended")
                time.sleep(0.25)


    def run(self) -> None:
        self.client_socket, address = self.socket.accept()
        self.target_name = Target.CART
        self.current_graph = self.node_util.create_graph()
        self.target = self.current_graph[50]
        self.current_node = self.current_graph[46]
        value = input(str())
        value = f"color.{value}"
        self.client_socket.send(value.encode("utf-8"))

        # Thread(target=self.down_cam, args=[]).start()
        Thread(target=self.top_cum, args=[]).start()
        Thread(target=self.graph_run, args=[]).start()


cl = TcpServer()
cl.run()
