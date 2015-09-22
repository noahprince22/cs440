import logging
import sys
import Queue
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

def is_undiscovered(x, y):
    if discovered_maze[y][x] is False:
        return True

def make_discovered(x, y):
    discovered_maze[y][x] = True

def get_neighbors(x, y):
    neighbors = []
    # find the right neighbor
    if is_walkable(x+1, y) and is_undiscovered(x+1, y):
        neighbors.append((x+1, y))
    if is_walkable(x-1, y) and is_undiscovered(x-1, y):
        neighbors.append((x-1, y))
    if is_walkable(x, y+1) and is_undiscovered(x, y+1):
        neighbors.append((x, y+1))
    if is_walkable(x, y-1) and is_undiscovered(x, y-1):
        neighbors.append((x, y-1))
    return neighbors

def set_parent(child, parent):
    # child and parents are 2-tuples
    # assumes adjacency
    parents_maze[child[1]][child[0]] = parent
    # parents_maze[y][x] = parent <-- less confuzzling

def manhattan_distance(begin, end):
    x = abs(begin[0] - end[0])
    y = abs(begin[1] - end[1])
    return (x + y)

# def dfs(goal, penalties, x, y, current_penalty):
#     if current_penalty >= penalties[y][x]:
#         return None
#     else:
#         penalties[y][x] = current_penalty
        
#     if goal[0] == x and goal[1] == y:
#         return []

#     paths = [explore(goal, penalties, x, y, current_penalty, 'l'),
#              explore(goal, penalties, x, y, current_penalty, 'r'),
#              explore(goal, penalties, x, y, current_penalty, 'u'),
#              explore(goal, penalties, x, y, current_penalty, 'd')]

#     # Get the shortest path
#     minlength = sys.maxint
#     path = None
#     for p in paths:
#         if p is not None and len(p) < minlength:
#             path = p
#             minlength = len(p)
    
#     return path

# def explore(goal, walkable_maze, x, y, current_penalty, direction):
#     if direction == 'r':
#         x-=1
#     elif direction == 'l':
#         x+=1
#     elif direction == 'u':
#         y-=1
#     elif direction == 'd':
#         y+=1

#     path = dfs(goal, walkable_maze, x, y, current_penalty + 1)

#     if path is None:
#         return None
    
#     path.append(direction)
#     return path

# def direction_to_int(direction):
#     if direction == 'l':
#         return 0
#     if direction == 'r':
#         return 1
#     if direction == 'u':
#         return 2
#     if direction == 'd':
#         return 3

# # Each of penalties needs to encompass every state at that point, so we must include current direction
# def dfs_direction(goal, penalties, x, y, direction, current_penalty):
#     index = direction_to_int(direction)
    
#     if current_penalty >= penalties[y][x][index]:
#         return None
#     else:
#         penalties[y][x][index] = current_penalty
        
#     if goal[0] == x and goal[1] == y:
#         return []

#     paths = [explore_turns(goal, penalties, x, y, direction, current_penalty, 'f'),
#              explore_turns(goal, penalties, x, y, direction, current_penalty, 'l'),
#              explore_turns(goal, penalties, x, y, direction, current_penalty, 'r')]

#     # Get the shortest path
#     minlength = sys.maxint
#     path = None
#     for p in paths:
#         if p is not None and len(p) < minlength:
#             path = p
#             minlength = len(p)
    
#     return path

# def explore_turns(goal, penalties, x, y, direction, current_penalty, action):
#     # Forward in current direction
#     if action == 'f':
#         if direction == 'l':
#             x-=1
#         elif direction == 'r':
#             x+=1
#         elif direction == 'u':
#             y-=1
#         elif direction == 'd':
#             y+=1

#     # Turn 90 degrees left
#     elif action == 'l':
#         if direction == 'l':
#             direction = 'd'
#         elif direction == 'r':
#             direction = 'u'
#         elif direction == 'u':
#             direction = 'l'
#         elif direction == 'd':
#             direction = 'r'

#     # Turn 90 degrees right
#     elif action == 'r':
#         if direction == 'l':
#             direction = 'u'
#         elif direction == 'r':
#             direction = 'd'
#         elif direction == 'u':
#             direction = 'r'
#         elif direction == 'd':
#             direction = 'l'

#     path = dfs_direction(goal, penalties, x, y, direction, current_penalty + 1)

#     if path is None:
#         return None
    
#     path.append(action)
#     return path

def BFS(start, goal):
    q = Queue.Queue()
    q.put(start)
    print "qsize:" + str(q.qsize())

    while q.qsize() is not 0:
        u = q.get() #dequeue
        #print "dequeue" + str(u)

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u[0],u[1]):
            q.put(neighbor)
            set_parent(neighbor, u)
        make_discovered(u[0],u[1])

        if u[0] == goal[0] and u[1] == goal[1]:
            print "BREAK"
            return True
    return False

def Greedy(start, goal):
    q = Queue.PriorityQueue()
    q.put((0, start))
    print "qsize:" + str(q.qsize())

    while q.qsize() is not 0:
        u = q.get()[1] #dequeue
        print "dequeue " + str(u)

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u[0],u[1]):
            q.put( (manhattan_distance(neighbor[0], neighbor[1]), neighbor))
            set_parent(neighbor, u)
        make_discovered(u[0],u[1])

        if u[0] == goal[0] and u[1] == goal[1]:
            print "BREAK"
            return True
    return False
    return

maze = [list(char for char in line.rstrip('\n')) for line in open('maze.txt')]
maze_width = len(maze[0])
maze_height = len(maze)
start = find("P")
goal = find(".")

# Test dfs regular
# Keep commented out to test dfs others. The printing of the maze changes the actual values on the maze

# penalties = [[sys.maxint if is_walkable(x,y) else 0 for x in range (0, maze_width)] for y in range(0, maze_height)]
# path = dfs(goal, penalties, start[0], start[1], 0)

# x = goal[0]
# y = goal[1]

# test_maze = list(maze)

# for z in test_maze:
#     for k in z:
#         print k,

#     print

# i = 0
# for p in path:
#     if p == 'u':
#         y+=1
#     elif p == 'd':
#         y-=1
#     elif p == 'l':
#         x-=1
#     elif p == 'r':
#         x+=1

#     i +=1
#     test_maze[y][x] = 'o'

# for x in test_maze:
#     for y in x:
#         print y,

#     print


# Test for directional dfs
# Test dfs regular
# Keep commented out to test dfs others. The printing of the maze changes the actual values on the maze

# sys.setrecursionlimit(10000)
# penalties = [[[sys.maxint if is_walkable(x,y) else 0 for z in range (0,4)] for x in range (0, maze_width)] for y in range(0, maze_height)] 
# path = dfs_direction(goal, penalties, start[0], start[1], 'u', 0)
# print path

# test_maze = list(maze)

# # Direcional dfs returns a list of the actions taken with the earlier actions being at the end of the list
# # Here we reverse the list and then trace back from the start the path taken
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


maze_walkable_bool = [[is_walkable(x, y) for x in range(0,maze_width)] for y in range(0,maze_height)]

# Create 2d array of undiscovered areas
discovered_maze = [[False for x in range(0,maze_width)] for y in range(0,maze_height)]
parents_maze = [[None for x in range(0,maze_width)] for y in range(0,maze_height)]

print "start: " + str(start) + ". goal: " + str(goal)

if Greedy(start, goal) is True:
    print "yay"
else:
    print "nay"

# trace way home
# add goal to pathlist
# while last item of pathlist is not start...
#
path = []
path.append(goal)
while path[-1] is not start:
    parent = parents_maze[path[-1][1]][path[-1][0]]
    path.append(parent)
print path

for y in range(0, maze_height):
    for x in range(0, maze_width):
        if is_walkable(x,y) is False:
            sys.stdout.write("%")
        elif is_undiscovered(x,y) is True:
            sys.stdout.write(" ")
        else:
            sys.stdout.write(".")
    sys.stdout.write("\n")

print "-" *  20

for y in range(0, maze_height):
    for x in range(0, maze_width):
        if is_walkable(x,y) is False:
            sys.stdout.write("%")
        elif (x, y) in path:
            sys.stdout.write(".")
        else:
            sys.stdout.write(" ")
    sys.stdout.write("\n")
