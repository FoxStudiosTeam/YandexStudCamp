from pyray import *
import math

CELL_SIZE = (40, 40)

SCREEN_SIZE = (800, 800)

init_window(SCREEN_SIZE[0], SCREEN_SIZE[1], "ray")

GRID_SIZE = (20, 20)

grid_data = [[False for _ in range(GRID_SIZE[1])] for _ in range(GRID_SIZE[0])]

for i in range(0):
    grid_data[10][5 + i] = True

def draw_cell(x, y, color):
    draw_rectangle(x * CELL_SIZE[0], y * CELL_SIZE[1], CELL_SIZE[0], CELL_SIZE[1], color)


def draw_grid():
    for x in range(0, GRID_SIZE[0]):
        for y in range(0, GRID_SIZE[1]):
            if grid_data[x][y]:
                draw_cell(x, y, BLACK)
    for x in range(0, GRID_SIZE[0]+1):
        draw_line(x * CELL_SIZE[0], 0, x * CELL_SIZE[0], 
                  GRID_SIZE[1] * CELL_SIZE[1], GRAY)
    for y in range(0, GRID_SIZE[1]+1):
        draw_line(0, y * CELL_SIZE[0], 
                  GRID_SIZE[0] * CELL_SIZE[0], y * CELL_SIZE[1], GRAY)
    

def unchecked_cell(x, y, c=GREEN):
    draw_rectangle(
        math.ceil(x * CELL_SIZE[0] - CELL_SIZE[0] / 8), math.ceil(y * CELL_SIZE[1] - CELL_SIZE[1] / 8), math.ceil(CELL_SIZE[0]/4), math.ceil(CELL_SIZE[1]/4), c)


def has_intersection(start, end, diag_check=False):
    x1 = start[0] + 0.5
    y1 = start[1] + 0.5
    x2 = end[0] + 0.5
    y2 = end[1] + 0.5
    if y1 == y2:
        for x in range(math.floor(min(x1, x2)), math.ceil(max(x1, x2))):
            unchecked_cell(x + 0.5, y1)
        return
    if x1 == x2:
        for y in range(math.floor(min(x1, x2)), math.ceil(max(x1, x2))):
            unchecked_cell(x1, y + 0.5)
        return
    if x1 == x2 or y1 == y2: return False


    if abs(x1 - x2) > abs(y1 - y2):
        positivex = True if x1 < x2 else False
        prevx = math.floor(min(x1, x2)) # if (x1 - x2 <= 0) == (y1 - y2 <= 0) else max(x1, x2)
        m = (y2 - y1) / (x2 - x1)
        y = min(y1, y2)
        
        unchecked_cell(prevx, y, RED)

        while y <= max(y1, y2):
            # y = mx + b
            # x = (y - b) / m
            x = (y - y1 + 0.5) / m + x1
            #if not (min(x1, x2) < x < max(x1, x2)):
            #    break
            unchecked_cell(x, y + 0.5)
            #if diag_check and abs(x) % 1 < 0.001:
            #    if (min(x1, x2) < x < max(x1, x2)):
            #        unchecked_cell(x, y + 0.5, RED)
            #        unchecked_cell(x - 0.5, y, RED)
            #        unchecked_cell(x + 0.5, y, RED)
            #        unchecked_cell(x - 0.5, y + 1, RED)
            #        unchecked_cell(x + 0.5, y + 1, RED)
            #mix = min(prevx, math.floor(x))
            #mx = max(prevx, math.floor(x))
            #for nx in range(mix, mx + 1):
            #    unchecked_cell(nx + 0.5, y)
            #    if not (min(x1, x2) < x < max(x1, x2)):
            #        break
            #unchecked_cell(mix + 0.5, y, RED)
            #
            #unchecked_cell(prevx, y - 0.5)
            #prevx = math.floor(x)
            y += 1
        







START_POS = (0, 0)

while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    mouse_x = get_mouse_x()
    mouse_y = get_mouse_y()
    mouse_in_grid = (round((mouse_x - CELL_SIZE[0] * 0.5) / CELL_SIZE[0] ), round((mouse_y - CELL_SIZE[1] * 0.5) / CELL_SIZE[1]))
    #draw_cell(mouse_in_grid[0], mouse_in_grid[1], RED)

    if is_mouse_button_pressed(0):
        START_POS = mouse_in_grid
    
    has_intersection(START_POS, mouse_in_grid)

    draw_grid()
    
    draw_line(START_POS[0] * CELL_SIZE[0] + round(CELL_SIZE[0] / 2), START_POS[1] * CELL_SIZE[1] + round(CELL_SIZE[1] / 2), 
              mouse_in_grid[0] * CELL_SIZE[0] + round(CELL_SIZE[0] / 2), mouse_in_grid[1] * CELL_SIZE[1] + round(CELL_SIZE[1] / 2), GREEN)
    #draw_line(START_POS[0] * CELL_SIZE[0], START_POS[1] * CELL_SIZE[1], 
    #            mouse_in_grid[0] * CELL_SIZE[0], mouse_in_grid[1] * CELL_SIZE[1], GREEN)
    
    end_drawing()
close_window()