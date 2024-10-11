from fs_move_simple import AStarPath, create_graph, Node
from tkinter import *

nodes = create_graph()
a_star_path = AStarPath(nodes)

queue = a_star_path.a_star_simple(nodes[0], nodes[5],nodes)

root = Tk()
width = 800
height = 600

canvas = Canvas(root, width=width, height=height)

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

for node in nodes:
    x0 = node.x*10
    x1 = x0+10
    y0 = node.y*10
    y1 = y0+10


    if node.is_block == True:
        canvas.create_rectangle(x0, y0, x1, y1, fill='red')
    else:
        canvas.create_rectangle(x0,y0,x1,y1,fill='white')

path = []
while len(queue.queue) > 0:
    item : tuple[int, Node] = queue.get()
    path.append(item[1])

for i in range (len(path)-1):
    x0 = path[i].x*10 + 5
    y0 = path[i].y*10 + 5
    x1 = path[i+1].x*10 + 5
    y1 = path[i+1].y*10 + 5
    canvas.create_line(x0, y0, x1, y1, fill='blue', width=3)

canvas.pack()
root.mainloop()