import logging
import sys
logging.basicConfig(filename='happenings.log', level=logging.DEBUG)

def anyone_home_at(x,y):
    if x < 0 or x >= maze_width:
        return False
    if y < 0 or y >= maze_height:
        return False
    return True

def find(char):
    for y in range(1,maze_height):
        for x in range(1,maze_width):
            if maze[y][x] is char:
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

maze = [list(char for char in line.rstrip('\n')) for line in open('maze.txt')]
maze_width = len(maze[0])
maze_height = len(maze)
start = find("P")
goal = find(".")

maze_walkable_bool = [[is_walkable(x, y) for x in range(0,maze_width)] for y in range(0,maze_height)]

# Create 2d array of undiscovered areas
discovered_maze = [[(x,y) for x in range(0,maze_width)] for y in range(0,maze_height)]

print "sha la la"

state = start
#while state is not goal: