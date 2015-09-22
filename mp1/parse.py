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

