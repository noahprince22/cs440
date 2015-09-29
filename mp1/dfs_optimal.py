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

def dfs(goal, penalties, x, y, current_penalty, expanded_nodes):
    if current_penalty >= penalties[y][x]:
        return None
    else:
        penalties[y][x] = current_penalty
        
    if goal[0] == x and goal[1] == y:
        return []

    paths = [explore(goal, penalties, x, y, current_penalty, 'l', expanded_nodes),
             explore(goal, penalties, x, y, current_penalty, 'r', expanded_nodes),
             explore(goal, penalties, x, y, current_penalty, 'u', expanded_nodes),
             explore(goal, penalties, x, y, current_penalty, 'd', expanded_nodes)]

    # Get the shortest path
    minlength = sys.maxint
    path = None
    for p in paths:
        if p is not None and len(p) < minlength:
            path = p
            minlength = len(p)
    
    return path

def explore(goal, walkable_maze, x, y, current_penalty, direction, expanded_nodes):
    if direction == 'r':
        x-=1
    elif direction == 'l':
        x+=1
    elif direction == 'u':
        y-=1
    elif direction == 'd':
        y+=1

    expanded_nodes[0] = expanded_nodes[0] + 1
    path = dfs(goal, walkable_maze, x, y, current_penalty + 1, expanded_nodes)

    if path is None:
        return None
    
    path.append(direction)
    return path

def direction_to_int(direction):
    if direction == 'l':
        return 0
    if direction == 'r':
        return 1
    if direction == 'u':
        return 2
    if direction == 'd':
        return 3

# Each of penalties needs to encompass every state at that point, so we must include current direction
def dfs_direction(goal, penalties, x, y, direction, current_penalty):
    index = direction_to_int(direction)
    
    if current_penalty >= penalties[y][x][index]:
        return None
    else:
        penalties[y][x][index] = current_penalty
        
    if goal[0] == x and goal[1] == y:
        return []

    paths = [explore_turns(goal, penalties, x, y, direction, current_penalty, 'f'),
             explore_turns(goal, penalties, x, y, direction, current_penalty, 'l'),
             explore_turns(goal, penalties, x, y, direction, current_penalty, 'r')]

    # Get the shortest path
    minlength = sys.maxint
    path = None
    for p in paths:
        if p is not None and len(p) < minlength:
            path = p
            minlength = len(p)
    
    return path

def explore_turns(goal, penalties, x, y, direction, current_penalty, action):
    # Forward in current direction
    if action == 'f':
        if direction == 'l':
            x-=1
        elif direction == 'r':
            x+=1
        elif direction == 'u':
            y-=1
        elif direction == 'd':
            y+=1

    # Turn 90 degrees left
    elif action == 'l':
        if direction == 'l':
            direction = 'd'
        elif direction == 'r':
            direction = 'u'
        elif direction == 'u':
            direction = 'l'
        elif direction == 'd':
            direction = 'r'

    # Turn 90 degrees right
    elif action == 'r':
        if direction == 'l':
            direction = 'u'
        elif direction == 'r':
            direction = 'd'
        elif direction == 'u':
            direction = 'r'
        elif direction == 'd':
            direction = 'l'

    path = dfs_direction(goal, penalties, x, y, direction, current_penalty + 1)

    if path is None:
        return None
    
    path.append(action)
    return path

maze = [list(char for char in line.rstrip('\n')) for line in open('openmaze.txt')]
maze_width = len(maze[0])
maze_height = len(maze)
start = find("P")
goal = find(".")

maze_walkable_bool = [[[is_walkable(x, y) for x in range(0,maze_width)] for y in range(0,maze_height)]]

# Test dfs regular
penalties = [[sys.maxint if is_walkable(x,y) else 0 for x in range (0, maze_width)] for y in range(0, maze_height)]
expanded_nodes = [0]
path = dfs(goal, penalties, start[0], start[1], 0, expanded_nodes)
print "expanded %s" % expanded_nodes[0]
print "Cost %s" % len(path)

x = goal[0]
y = goal[1]

test_maze = list(maze)

for z in test_maze:
    for k in z:
        print k,

    print

i = 0
for p in path:
    if p == 'u':
        y+=1
    elif p == 'd':
        y-=1
    elif p == 'l':
        x-=1
    elif p == 'r':
        x+=1

    i +=1
    test_maze[y][x] = 'o'

for x in test_maze:
    for y in x:
        print y,

    print


# Test for directional dfs
# sys.setrecursionlimit(10000)
# penalties = [[[sys.maxint if is_walkable(x,y) else 0 for z in range (0,4)] for x in range (0, maze_width)] for y in range(0, maze_height)] 
# path = dfs_direction(goal, penalties, start[0], start[1], 'u', 0)
# print path

# test_maze = list(maze)

# direction = 'u'
# x = start[0]
# y = start[1]
# path.reverse()
# for action in path:
#     if action == 'f':
#         if direction == 'l':
#             x-=1
#         elif direction == 'r':
#             x+=1
#         elif direction == 'u':
#             y-=1
#         elif direction == 'd':
#             y+=1

#     elif action == 'l':
#         if direction == 'l':
#             direction = 'd'
#         elif direction == 'r':
#             direction = 'u'
#         elif direction == 'u':
#             direction = 'l'
#         elif direction == 'd':
#             direction = 'r'

#     elif action == 'r':
#             if direction == 'l':
#                 direction = 'u'
#             elif direction == 'r':
#                 direction = 'd'
#             elif direction == 'u':
#                 direction = 'r'
#             elif direction == 'd':
#                 direction = 'l'

#     test_maze[y][x] = 'o'


# for x in test_maze:
#     for y in x:
#         print y,

#     print

