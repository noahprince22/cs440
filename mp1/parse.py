import graph
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

def dfs(goal, walkable_maze, x, y):
    if walkable_maze[y][x] == False or not anyone_home_at(x,y):
        return None
        
    if goal[0] == x and goal[1] == y:
        return []
    
    walkable_maze[y][x] = False

    paths = [explore(goal, walkable_maze, x, y, 'l'),
             explore(goal, walkable_maze, x, y, 'r'),
             explore(goal, walkable_maze, x, y, 'u'),
             explore(goal, walkable_maze, x, y, 'd')]

    # Get the shortest path
    path = []
    minlength = sys.maxint
    for p in paths:
        if p is not None and len(p) < minlength:
            minlength = len(p)
            path = p
    
    walkable_maze[y][x] = True

    return path

def explore(goal, walkable_maze, x, y, direction):
    if direction == 'r':
        x+=1
    elif direction == 'l':
        x-=1
    elif direction == 'u':
        y+=1
    elif direction == 'd':
        y-=1

    result = dfs(goal, walkable_maze, x, y)

    if result is None:
        return None

    print "%s %s %s %s" % (x, y, direction, result)

    result.append(direction)

    return result


maze = [list(char for char in line.rstrip('\n')) for line in open('maze.txt')]
maze_width = len(maze[0])
maze_height = len(maze)
start = find("P")
goal = find(".")

maze_walkable_bool = [[is_walkable(x, y) for x in range(0,maze_width)] for y in range(0,maze_height)]

print maze_walkable_bool

path = dfs(goal, maze_walkable_bool, start[0], start[1])
print path

