import logging
import sys
import Queue
import numpy
logging.basicConfig(filename='happenings.log', level=logging.DEBUG)

# logging: log events for debugging and review, NOT for final output
# sys: for console output, NOT for final output
# Queue: Queue and PriorityQueue data structures used in search implementations
# numpy: only used for tuple arithmetic

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

def penalty(walking_to, walking_from, orientation):
    # orientation := initial orientation
    turns = 0
    # no turn and walk -> 1 penalty

    # 1 turn and walk -> 2 penalty


    # 2 turn and walk -> 3 penalty


    return penalty

def setup(filename):
    global maze
    global maze_width
    global maze_height
    global start
    global goal
    global maze_walkable_bool
    global discovered_maze
    global parents_maze
    maze = [list(char for char in line.rstrip('\n')) for line in open(filename)]
    maze_width = len(maze[0])
    maze_height = len(maze)
    start = find("P")
    goal = find(".")
    maze_walkable_bool = [[is_walkable(x, y) for x in range(0,maze_width)] for y in range(0,maze_height)]
    discovered_maze = [[False for x in range(0,maze_width)] for y in range(0,maze_height)]
    parents_maze = [[None for x in range(0,maze_width)] for y in range(0,maze_height)]

def retrace():
    # trace way home
    # add goal to path (list)
    # while last item of path (list) is not start...
    path = []
    path.append(goal)
    while path[-1] is not start:
        parent = parents_maze[path[-1][1]][path[-1][0]]
        path.append(parent)

    print "Many paths walked..."

    for y in range(0, maze_height):
        for x in range(0, maze_width):
            if is_walkable(x,y) is False:
                sys.stdout.write("%")
            elif is_undiscovered(x,y) is True:
                sys.stdout.write(" ")
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")

    print "-" * maze_width

    print "... BUT THERE IS BUT ONE TRUE PATH!!!"

    for y in range(0, maze_height):
        for x in range(0, maze_width):
            if is_walkable(x,y) is False:
                sys.stdout.write("%")
            elif (x, y) in path:
                sys.stdout.write(".")
            else:
                sys.stdout.write(" ")
        sys.stdout.write("\n")


def BFS(filename):
    setup(filename)
    q = Queue.Queue()
    q.put(start)

    while q.qsize() is not 0:
        u = q.get() #dequeue

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u[0],u[1]):
            q.put(neighbor)
            set_parent(neighbor, u)
        make_discovered(u[0],u[1])

        if u[0] == goal[0] and u[1] == goal[1]:
            return True
    return False

def run_BFS(filename):
    if BFS(filename) is True:
        print "yay"
        retrace()
        print "Breadth-First Search:"
    else:
        print "nay"

def Greedy(filename, penalize):
    setup(filename)
    q = Queue.PriorityQueue()
    q.put((0, start))

    while q.qsize() is not 0:
        u = q.get()[1] #dequeue

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u[0],u[1]):
            q.put( (manhattan_distance(neighbor, goal) + penalty(neighbor, u, "left"), neighbor))
            set_parent(neighbor, u)
        make_discovered(u[0],u[1])

        if u[0] == goal[0] and u[1] == goal[1]:
            return True
    return False

def run_Greedy(filenamep, penalize=False):
    if Greedy(filename, penalize) is True:
        print "yay"
        print "Greedy Best-First Search:"
        retrace()
    else:
        print "nay"

def A_Star(filename):
    setup(filename)
    q = Queue.PriorityQueue()
    q.put((0, start))
    distance_travelled = 0

    while q.qsize() is not 0:
        u = q.get()[1] #dequeue
        distance_travelled = distance_travelled + 1

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u[0],u[1]):
            q.put( (manhattan_distance(neighbor, goal) + distance_travelled, neighbor))
            set_parent(neighbor, u)
        make_discovered(u[0],u[1])

        if u[0] == goal[0] and u[1] == goal[1]:
            return True
    return False

def run_Greedy(filename):
    if A_Star(filename) is True:
        print "yay"
        print "A* Search:"
        retrace()
    else:
        print "nay"

run_Greedy("maze.txt")

