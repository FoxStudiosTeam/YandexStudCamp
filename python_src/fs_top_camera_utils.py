from typing import Tuple


class TopCameraUtils:
    def __init__(self, x_pic: int, y_pic: int):
        self.x_pic = x_pic
        self.y_pic = y_pic

    # TODO: current_pos_from_neuro -> rn to normal name
    def calculate_current_pos(self, current_pos_from_neuro: Tuple[int, int]) -> Tuple[int, int]:
        neuro_x_pos = current_pos_from_neuro[0]
        graph_num_x = 8 * 4
        neuro_y_pos = current_pos_from_neuro[1]
        graph_num_y = 6 * 4

        virtual_node_size_x = self.calculate_virtual_node_size(self.x_pic, graph_num_x)
        virtual_node_size_y = self.calculate_virtual_node_size(self.y_pic, graph_num_y)

        node_x = self.calculate_node_pos(neuro_x_pos, virtual_node_size_x)

        node_y = self.calculate_node_pos(neuro_y_pos, virtual_node_size_y)

        return node_x, node_y

    def calculate_virtual_node_size(self, pos: int, graph_num: int) -> int:
        return pos // graph_num

    def calculate_node_pos(self, pos: int, virtual_node_size):
        return pos // virtual_node_size



