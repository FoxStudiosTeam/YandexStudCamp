from fs_move_simple import AStarPath, create_graph, Node, Direction
from tkinter import *
import time

nodes = create_graph()
a_star_path = AStarPath()

# queue = a_star_path.a_star_simple(nodes[0], nodes[510],nodes)
path = a_star_path.a_star_simple(nodes[50], nodes[372],nodes)
#path = a_star_path.a_star_simple(nodes[0], nodes[526])

root = Tk()

canvas = Canvas(root)

offset_x = 0
offset_y = 0
maxX: Node = None
maxY: Node = None

i = 0
for node in nodes:
    if i == 0:
        maxX = node
        maxY = node

    if maxX.x < node.x:
        maxX = node
    if maxY.y < node.y:
        maxY = node
    i += 0

# end_node = ((queue.queue)[len(queue.queue)-1])[1]
end_node = path[len(path) - 1]
for node in nodes:
    x0 = node.x * 10
    x1 = x0 + 10
    y0 = node.y * 10
    y1 = y0 + 10
    color = 'white'
    if node == end_node:
        canvas.create_rectangle(x0, y0, x1, y1, fill='orange')

    elif node.is_block == True:
        canvas.create_rectangle(x0, y0, x1, y1, fill='red')
    else:
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)

# path = []
# while len(queue.queue) > 0:
#     item : tuple[int, Node] = queue.get()
#     path.append(item[1])

# path.reverse()


# for i in range (len(path)-1):
#     x0 = path[i].x*10 + 5
#     y0 = path[i].y*10 + 5
#     x1 = path[i+1].x*10 + 5
#     y1 = path[i+1].y*10 + 5
#     canvas.create_line(x0, y0, x1, y1, fill='blue', width=3)


canvas.pack()


for i in range (len(path)-1):
    elem = path[i]

    x0 = elem.x * 10 + 5
    y0 = elem.y*10 + 5
    x1 = path[i+1].x*10 + 5
    y1 = path[i+1].y*10 + 5

    fill_color = 'black'
    if elem.direction == Direction.FORWARD:
        fill_color = 'blue'
    elif elem.direction == Direction.BACK:
        fill_color = 'red'
    elif elem.direction == Direction.BACK_LEFT:
        fill_color = 'orange'
    elif elem.direction == Direction.BACK_RIGHT:
        fill_color = 'green'
    elif elem.direction == Direction.FORWARD_LEFT:
        fill_color = 'purple'
    elif elem.direction == Direction.FORWARD_RIGHT:
        fill_color = 'cyan'
    elif elem.direction == Direction.LEFT:
        fill_color = 'pink'
    elif elem.direction == Direction.RIGHT:
        fill_color = 'yellow'

    print(f'x :{elem.x} y: {elem.y} direction: {elem.direction}')

    line = canvas.create_line(x0, y0, x1, y1, fill=fill_color, width=3)
    canvas.update()
    time.sleep(0.25)

root.mainloop()