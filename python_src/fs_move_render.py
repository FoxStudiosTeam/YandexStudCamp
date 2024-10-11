from python_src.fs_move_simple import AStarPath, create_graph, Node
from tkinter import *

nodes = create_graph()
a_star_path = AStarPath(nodes)

queue = a_star_path.a_star_simple(nodes[0], nodes[10],nodes)

root = Tk()
width = 600
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
    x0 = node.x + node.x*20
    x1 = x0+20
    y0 = node.y + node.y*20
    y1 = y0+20


    if node.is_block == True:
        canvas.create_rectangle(x0, y0, x1, y1, fill='red')
    else:
        canvas.create_rectangle(x0,y0,x1,y1,fill='white')

canvas.pack()
root.mainloop()
