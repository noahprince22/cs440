import graph
import logging
import sys
logging.basicConfig(filename='happenings.log', level=logging.DEBUG)

def anyone_home_at(x,y):
    if x < 0 or x >= maze_width:
        return False
    if y < 0 and y >= maze_height:
        return False
    return True

def find(char):
    for y in range(1,maze_height):
        for x in range(1,maze_width):
            if whats_at(x,y) is char:
                return (x,y)
                # "+1" accounting for x,y starting at 0

def is_walkable(x, y):
    if maze[y][x] in [' ','.','P']:
        return True
    else: return False

def manhattan_distance(begin, end):
    x = abs(begin[0] - end[0])
    y = abs(begin[1] - end[1])
    return (x + y)

raw_maze = [list(char for char in line.rstrip('\n')) for line in open('maze.txt')]
maze_width = len(maze[0])
maze_height = len(maze)
start = find("P")
goal = find(".")

maze_walkable_bool = [[is_walkable(x, y) for x in range(0,maze_width)] for y in range(0,maze_height)]

maze_nodes_filtered = []

for row in maze_nodes:
    for node in row:
        x = node[1]
        y = node[0]
        if maze_walkable_bool[y][x] is True:
            maze_nodes_filtered.append(node)

# for y in maze_walkable_bool:
#     for x in y:
#         if x is True:
#             sys.stdout.write(' ')
#         else:
#             sys.stdout.write('%')
#     print("")
# This nearly replicates the original input maze. This proves that the 2D array is accurate.