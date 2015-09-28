import logging
import sys
import Queue
import numpy
import math

logging.basicConfig(filename='happenings.log', level=logging.DEBUG)
# logging: log events for debugging and review, NOT for final output

import sys
# sys: for console output, NOT for final output

import Queue
# Queue: Queue and PriorityQueue data structures used in search implementations

import numpy
# numpy: only used for tuple arithmetic

import collections
# used to create named tuple Point. Rationale: readability.
Point = collections.namedtuple('Point', 'x y')

logging.basicConfig(filename='happenings.log', level=logging.DEBUG)


def anyone_home_at(x, y):
    """
    :param x: int
    :param y: int
    :return: boolean
    """
    if x < 0 or x >= maze_width:
        return False
    if y < 0 or y >= maze_height:
        return False
    return True


def find(char):
    """
    :param char: string, ex: "P", "."
    :return: tuple (x, y), corresponding to node in maze 2-d array
    """
    for y in range(1, maze_height):
        for x in range(1, maze_width):
            if maze[y][x] is char:
                return Point(x, y)
                # "+1" accounting for x,y starting at 0


def is_walkable(x, y):
    """
    :param x: int
    :param y: int
    :return: boolean
    """

    if anyone_home_at(x, y) == False:
        return False

    if maze[y][x] in [' ', '.', 'P', 'G', 'g']:
        return True
    else:
        return False


def is_undiscovered(x, y):
    """
    :param x: int
    :param y: int
    :return: boolean
    """
    if discovered_maze[y][x] is False:
        return True
    else:
        return False


def make_discovered(x, y):
    """
    :param x: int
    :param y: int
    :return: nothing; manipulates global object
    """
    discovered_maze[y][x] = True


def get_neighbors(x, y):
    """
    :param x: int
    :param y: int
    :return: list of tuples: [(x_1, y_1) ... (x_n, y_n)]
    """
    neighbors = []
    # find the right neighbor
    if is_walkable(x + 1, y) and is_undiscovered(x + 1, y):
        neighbors.append(Point(x + 1, y))
    if is_walkable(x - 1, y) and is_undiscovered(x - 1, y):
        neighbors.append(Point(x - 1, y))
    if is_walkable(x, y + 1) and is_undiscovered(x, y + 1):
        neighbors.append(Point(x, y + 1))
    if is_walkable(x, y - 1) and is_undiscovered(x, y - 1):
        neighbors.append(Point(x, y - 1))
    return neighbors


def set_parent(child, parent):
    """
    :param child: tuple (x, y)
    :param parent: tuple (x, y)
    :return:
    """
    # child and parents are 2-tuples
    # assumes adjacency
    parents_maze[child.y][child.x] = parent
    # parents_maze[y][x] = parent <-- less confuzzling


def manhattan_distance(begin, end):
    x = abs(begin.x - end.y)
    y = abs(begin.y - end.y)
    return (x + y)


def penalty(walking_to, walking_from, initial_orientation, alternate_scheme=0):
    # when alternate_scheme is 0: move forward cost si 1, turn cost is 1
    # when alternate_scheme is 1: move forward cost is 1, turn cost is 2
    # when alternate_scheme is 2: move forward cost is 2, turn cost is 1
    """
    :param walking_to: tuple (x, y)
    :param walking_from: tuple (x, y)
    :param initial_orientation: string in ["L", "R", "U", "D"]
    :return: int i: 1 <= i <= 3
    """

    def where_you_walking(walking_to, walking_from):
        """
        :param walking_to: tuple (x, y)
        :param walking_from: tuple (x, y)
        :return: string in ["L", "R", "U", "D"]
        """
        vector = tuple(numpy.subtract(walking_to, walking_from))
        # vector[0] := x
        if vector == (1, 0):
            direction = "L"
        elif vector == (-1, 0):
            direction = "R"
        # vector[0] := y
        elif vector == (0, 1):
            direction = "U"
        elif vector == (0, -1):
            direction = "D"
        return direction

    # inner functions ^ v
    def how_many_turns(start_orientation, end_orientation):
        """
        :param start_orientation: string: "L" := Left, "R" := Right, "U" := Up, "D" := Down
        :param end_orientation: string: ^ ^ ^ ^
        :return: tuple, (int, string). Int: 0 <= i <= 2. String in ["L","R","U","D"]
        """
        if start_orientation not in ["L", "R", "U", "D"] or end_orientation not in ["L", "R", "U", "D"]:
            print "ORIENTATION ERROR"
            return 1
        else:
            if start_orientation is end_orientation:
                # already facing the right way, so no turns
                return 0
            elif (start_orientation in ["L", "R"] and end_orientation in ["U", "D"]) or (
                    start_orientation in ["U", "D"] and end_orientation in ["L", "R"]):
                # 90 deg turn
                return 1
            elif start_orientation is not end_orientation and (
                (start_orientation in ["L", "R"] and end_orientation in ["L", "R"]) or (
                    start_orientation in ["U", "D"] and end_orientation in ["U", "D"])):
                # 180 deg turn
                return 2
            else:
                print "Weird error at how_many_turns. Check, check it out. This shouldn't be happening."
                return 0

    # -------- back to main function
    new_direction = where_you_walking(walking_to, walking_from)
    turns = how_many_turns(initial_orientation, new_direction)
    if alternate_scheme == 0:
        # sys.stdout.write(str(turns + 1))
        return turns + 1, new_direction
    elif alternate_scheme == 1:
        # sys.stdout.write(str(turns + 2))
        return turns + 2, new_direction
    elif alternate_scheme == 2:
        # sys.stdout.write(str(2*turns + 1))
        return 2 * turns + 1, new_direction
    else:
        print "ERROR. Don't be dumb. Check the penalty function."
        # 1 point penalty per turn, so no need to modify.


def get_wall_density():
    total = 0
    for y in maze:
        for x in y:
            if x in ["%", "G", "g"]:
                total += 1

    return float(total) / (maze_width * maze_height)


def wall_density_heuristic(start, goal):
    """
    :param start_vertex: Point namedtuple
    :param goal_vertex: Point namedtuple
    :return: float
    """
    total = 0

    for y in range(min(start.y, goal.y), max(start.y, goal.y)):
        for x in range(min(start.x, goal.x), max(start.x, goal.x)):
            if maze[y][x] is "%":
                total += 1

    area = abs((start.y - goal.y) * (start.x - goal.x))
    if area is not 0:
        print float(total) / area
        return float(total) / area
    else:
        return 0


def setup(filename):
    """
    :param filename: string, ex: "maze.txt"
    :return: nothing; sets up global objects to be manipulated by search funcs
    """
    global maze
    global maze_width
    global maze_height
    global start
    global goal
    global maze_walkable_bool
    global discovered_maze
    global parents_maze
    global turn_penalty_maze  # used for debugging
    global direction_maze  # used for debugging
    global distance_maze  # used for debugging
    maze = [list(char for char in line.rstrip('\n')) for line in open(filename)]
    maze_width = len(maze[0])
    maze_height = len(maze)
    start = find("P")
    goal = find(".")
    maze_walkable_bool = [[is_walkable(x, y) for x in range(0, maze_width)] for y in range(0, maze_height)]
    discovered_maze = [[False for x in range(0, maze_width)] for y in range(0, maze_height)]
    parents_maze = [[None for x in range(0, maze_width)] for y in range(0, maze_height)]
    turn_penalty_maze = [[0 for x in range(0, maze_width)] for y in range(0, maze_height)]
    direction_maze = [[None for x in range(0, maze_width)] for y in range(0, maze_height)]
    distance_maze = [[0 for x in range(0, maze_width)] for y in range(0, maze_height)]


def retrace(turns=False):
    # trace way home
    # add goal to path (list)
    # while last item of path (list) is not start...
    path = []
    path.append(goal)
    while path[-1] is not start:
        parent = parents_maze[path[-1][1]][path[-1][0]]
        path.append(parent)

    print "Many paths walked..."

    number_of_expanded_nodes = 0

    for y in range(0, maze_height):
        for x in range(0, maze_width):
            if is_walkable(x, y) is False:
                sys.stdout.write("%")
            elif is_undiscovered(x, y) is True:
                sys.stdout.write(" ")
            else:
                sys.stdout.write(".")
                number_of_expanded_nodes += 1
        sys.stdout.write("\n")

    cost = len(path)  # may or may not include turn costs depending on context
    print "Cost: " + str(cost)
    # this Cost printed is the path cost, independent of turn cost

    print "Number of expanded nodes: " + str(number_of_expanded_nodes)

    print "-" * maze_width

    print "... BUT THERE IS BUT ONE TRUE PATH!!!"

    cost = 0
    for y in range(0, maze_height):
        for x in range(0, maze_width):
            if is_walkable(x, y) is False:
                sys.stdout.write("%")
            elif (x, y) in path:
                sys.stdout.write(".")
                cost += 1
            else:
                sys.stdout.write(" ")
        sys.stdout.write("\n")

    print "Total cost: %s" % cost

    if turns is True:
        print "-" * maze_width

        print "Penalty"

        for y in range(0, maze_height):
            for x in range(0, maze_width):
                if is_walkable(x, y) is False:
                    sys.stdout.write("%")
                elif (x, y) in path:
                    # elif turn_penalty_maze[y][x] > 0:
                    penalty = turn_penalty_maze[y][x]  # completely local
                    sys.stdout.write(str(penalty))
                    cost += penalty
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")

        print "Cum. cost incl. turn costs: " + str(cost)

        print "-" * maze_width

        print "Directions"

        for y in range(0, maze_height):
            for x in range(0, maze_width):
                if is_walkable(x, y) is False:
                    sys.stdout.write("%")
                # elif direction_maze[y][x] is not None:
                elif (x, y) in path:
                    sys.stdout.write(direction_maze[y][x])
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")


def DFS(filename):
    setup(filename)
    s = Queue.LifoQueue()
    s.put(start)

    num_expanded = 0
    while s.qsize() is not 0:
        num_expanded += 1
        u = s.get()  # dequeue

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u.x, u.y):
            s.put(neighbor)
            set_parent(neighbor, u)
        make_discovered(u.x, u.y)

        if u.x == goal.x and u.y == goal.y:
            print "Expanded %s" % num_expanded
            return True

    return False


def run_DFS(filename):
    if DFS(filename) is True:
        print "yay"
        retrace()
        print "Depth-First Search:"
    else:
        print "nay"


def BFS(filename):
    setup(filename)
    q = Queue.Queue()
    q.put(start)

    num_expanded = 0
    while q.qsize() is not 0:
        num_expanded += 1
        u = q.get()  # dequeue

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u.x, u.y):
            q.put(neighbor)
            set_parent(neighbor, u)
        make_discovered(u.x, u.y)

        if u.x == goal.x and u.y == goal.y:
            print "Expanded %s" % num_expanded
            return True
    return False


def run_BFS(filename):
    if BFS(filename) is True:
        print "yay"
        retrace()
        print "Breadth-First Search:"
    else:
        print "nay"


def Greedy(filename):
    setup(filename)
    q = Queue.PriorityQueue()
    q.put((0, start))

    num_expanded = 0
    while q.qsize() is not 0:
        num_expanded += 1
        u = q.get()[1]  # dequeue
        # dequeue. u := Currently selected node

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u.x, u.y):
            q.put((manhattan_distance(neighbor, goal), neighbor))
            set_parent(neighbor, u)
        make_discovered(u.x, u.y)

        if u.x == goal.x and u.y == goal.y:
            print "Expanded %s" % num_expanded
            return True
    return False


def Greedy_with_turns(filename):
    setup(filename)
    q = Queue.PriorityQueue()
    q.put((0, start, "R"))

    while q.qsize() is not 0:
        next_up = q.get()
        # dequeue. u := Currently selected node
        u = next_up[1]
        old_orientation = next_up[2]

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u.x, u.y):
            turn_penalty, new_orientation = penalty(u, neighbor, old_orientation)
            q.put(((manhattan_distance(neighbor, goal) + turn_penalty), neighbor, new_orientation))
            set_parent(neighbor, u)
        make_discovered(u.x, u.y)

        if u.x == goal.x and u.y == goal.y:
            print "Expanded %s" % num_expanded
            return True
    return False


def run_Greedy(filename, turns=False):
    if turns is True:
        Greedy_with_turns(filename)
        print "Turn Penalty On"
    else:
        Greedy(filename)
    print "Greedy Best-First Search:"
    retrace()


def A_Star(filename, alternate_heuristic):
    setup(filename)
    q = Queue.PriorityQueue()
    q.put((0, start, 0))
    # format: (weight, point, distance from start to point)

    while q.qsize() is not 0:
        next_up = q.get()
        u = next_up[1]
        distance_travelled = next_up[2] + 1  # distance_travelled is node-specific

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u.x, u.y):
            if alternate_heuristic is False:
                q.put((manhattan_distance(neighbor, goal) + distance_travelled, neighbor, distance_travelled))
            else:  # else alternate_heuristic is True, then use different heuristic from the Manhattan distance once
                q.put(((wall_density_heuristic(neighbor, goal)) * (manhattan_distance(neighbor, goal) + distance_travelled),
                       neighbor, distance_travelled))
            set_parent(neighbor, u)
        make_discovered(u.x, u.y)

        if u.x == goal.x and u.y == goal.y:
            return True
    return False


def run_A_Star(filename, alternate_heuristic=False):
    if A_Star(filename, altnerate_heuristic) is True:
        print "yay"
        print "A* Search:"
        retrace()
    else:
        print "nay"


# True if there is no ghost at x, y
def no_ghost(x, y, ghost):
    theres_a_ghost = (x == ghost[0] and y == ghost[1])
    return not theres_a_ghost


def get_neighbors_ghost(x, y, ghost):
    neighbors = []
    # find the right neighbor
    if is_walkable(x + 1, y) and is_undiscovered(x + 1, y) and no_ghost(x + 1, y, ghost):
        neighbors.append(Point(x + 1, y))
    if is_walkable(x - 1, y) and is_undiscovered(x - 1, y) and no_ghost(x - 1, y, ghost):
        neighbors.append(Point(x - 1, y))
    if is_walkable(x, y + 1) and is_undiscovered(x, y + 1) and no_ghost(x, y + 1, ghost):
        neighbors.append(Point(x, y + 1))
    if is_walkable(x, y - 1) and is_undiscovered(x, y - 1) and no_ghost(x, y - 1, ghost):
        neighbors.append(Point(x, y - 1))
    return neighbors


def A_Star_Ghost(filename):
    setup(filename)
    ghost = find("G")
    dir_ghost = "r"
    q = Queue.PriorityQueue()
    q.put((0, start, 0, ghost, dir_ghost))

    nodes_expanded = 0

    while q.qsize() is not 0:
        nodes_expanded += 1

        element = q.get()
        u = element[1]  # dequeue
        distance_travelled = element[2] + 1
        ghost = element[3]
        ghost_dir = element[4]

        # Move the ghost
        x = ghost[0]
        y = ghost[1]

        if dir_ghost == 'r':
            if is_walkable(x + 1, y):
                ghost = (x + 1, y)
        else:
            dir_ghost = 'l'
            ghost = (x - 1, y)

        if dir_ghost == 'l':
            if is_walkable(x - 1, y):
                ghost = (x - 1, y)
        else:
            dir_ghost = 'r'
            ghost = (x + 1, y)

        # for all neighbors: 1. adjacent, 2. unexplored
        # note + tuple() creates a deep copy, which we need to preserve state
        # same with the string
        for neighbor in get_neighbors_ghost(u.x, u.y, ghost):
            q.put((manhattan_distance(neighbor, goal) + distance_travelled, neighbor,
                   distance_travelled, ghost + tuple(), dir_ghost + ""))
            set_parent(neighbor, u)
            make_discovered(u.x, u.y)

        if u.x == goal.x and u.y == goal.y:
            print "NODES EXPANDED: %s" % nodes_expanded
            return True
    return False


def run_A_Star_Ghost(filename):
    if A_Star_Ghost(filename) is True:
        print "yay"
        print "A* Search WITH ghost:"
        retrace()
    else:
        print "nay"


def A_Star_Hardmode_Ghost(filename):
    setup(filename)
    ghost = find("G")
    dir_ghost = "r"
    q = Queue.PriorityQueue()
    q.put((0, start, 0, ghost, dir_ghost))

    nodes_expanded = 0

    while q.qsize() is not 0:
        nodes_expanded += 1

        element = q.get()
        u = element[1]  # dequeue
        distance_travelled = element[2] + 1
        ghost = element[3]
        ghost_dir = element[4]

        # Move the ghost
        # In this implementation, the ghost chases pacman 
        ghost_neighbors = get_neighbors(ghost[0], ghost[1])
        min_distance = sys.maxint
        min_neighbor = ghost_neighbors[0]
        for neighbor in ghost_neighbors:
            if manhattan_distance(neighbor, u) < min_distance:
                min_distance = manhattan_distance(neighbor, u)
                min_neighbor = neighbor

        ghost = min_neighbor

        # for all neighbors: 1. adjacent, 2. unexplored
        # note + tuple() creates a deep copy, which we need to preserve state
        # same with the string
        for neighbor in get_neighbors_ghost(u.x, u.y, ghost):
            q.put((manhattan_distance(neighbor, goal) + distance_travelled, neighbor,
                   distance_travelled, ghost + tuple(), dir_ghost + ""))
            set_parent(neighbor, u)
            make_discovered(u.x, u.y)

        if u.x == goal.y and u.y == goal.y:
            print "NODES EXPANDED: %s" % nodes_expanded
            return True

    return False


def run_A_Star_Hardmode_Ghost(filename):
    if A_Star_Hardmode_Ghost(filename) is True:
        print "yay"
        print "A* Search WITH ghost:"
        retrace()
    else:
        print "nay"


def A_Star_with_turns(filename, alternate_scheme, alternate_heuristic):
    # alternate_scheme and alternate_heuristic are false by default, used for problem 1.2
    setup(filename)
    q = Queue.PriorityQueue()
    q.put((0, start, "R", 0))
    distance_travelled = 0
    direction_maze[start.y][start.x] = "R"

    while q.qsize() is not 0:
        next_up = q.get()
        # dequeue. u := Currently selected node
        u = next_up[1]
        old_orientation = next_up[2]

        # distance_travelled = distance_travelled + 1
        distance_travelled = next_up[3] + 1

        if u.x == goal.x and u.y == goal.y:
            return True

        # for all neighbors: 1. adjacent, 2. unexplored
        for neighbor in get_neighbors(u.x, u.y):
            turn_penalty, new_orientation = penalty(u, neighbor, old_orientation, alternate_scheme)
            if alternate_heuristic is False:
                q.put((
                      manhattan_distance(neighbor, goal) + distance_travelled + turn_penalty, neighbor, new_orientation,
                      distance_travelled))
            else:  # else alternate_heuristic is True, then use different heuristic from the Manhattan distance once
                q.put(((wall_density_heuristic(neighbor, goal)) * (
                manhattan_distance(neighbor, goal) + distance_travelled) + turn_penalty, neighbor, new_orientation,
                       distance_travelled))
            set_parent(neighbor, u)
            turn_penalty_maze[u.y][u.x] = turn_penalty
            direction_maze[neighbor.y][neighbor.x] = new_orientation
        make_discovered(u.x, u.y)
    return False


def run_A_Star(filename, turns=False, alternate_scheme=0, alternate_heuristic=False):
    print "A* Search:"
    if turns is True:
        A_Star_with_turns(filename, alternate_scheme, alternate_heuristic)
        print "Turn Penalty On"
        retrace(True)
    else:
        A_Star(filename, alternate_heuristic)
        retrace(False)


# run_Greedy("maze.txt", False)
# run_Greedy("maze.txt", True)

# run_A_Star("smallmaze.txt", True, 1, False)
# run_A_Star("smallmaze.txt", True, 2)

# run_A_Star("bigmaze_for_turns.txt", True, 2, True)
run_A_Star("mediummaze.txt", False, 0, True)
# run_BFS("maze.txt")

# run_A_Star_Hardmode_Ghost("ghostbig.txt")
"""
for 1.1:
(open) maze.txt
mediummaze.txt
bigmaze.txt

for 1.2:
smallmaze.txt
bigmaze_for_turns.txt

USE THE RIGHT INPUT
"""

"""
1801L1;tCL1;1CCLLLtfifLtt11CC;iCG0L1t1GL;Lf;i11ffCCCf0L;t1fGtfLf1CC;ffCftLC1tG11tCCfCCffGCt11Cft1Cftti1LL1t1fi;iLi:1Lt11fCLi11tfttfCfCLttf1t1:tt
t1;fG1,iiLttt1fCfC8tLL;iffi1LGC:G1:ftLLLi1f1ifLtiitt1t1L8LLtftGC1tfC0CGCfLGiiftf1C1fCGCt1tLftLfCL;fLtfLCLff1;Lft11ti:,:11itt1;;;i1t1ii;f0Li1iGCf
CLfGLLifGL1CGLGC0L1Lt1tCC1iC8f1fLC80LLLfGCLGLt:Lt1fGCCC,;tCG1tGGLCfitLL1t11CGfff1ifGGGCCGL1tLCL1ifCCft1i;11;:1tt1tfttfii1t1i11ttft1i,1L1,:it0Ltf
f0ttGffLGLt;f0C88CiGLL08L:tfff1ti1CLCGGfCG8ft;t1i;1CGti0Cf;1ifti:iL1ii;t1LtiLC1LGLfC00800L11f11CCLL1;;;;i1tCC1CCfifCtCfi1t;1f;;Lti1LGL;;fft1i,;t
tf0110GtfLf11i:f8ttCLfGf,C@1tCfC0CLLit0f;1fC1C1iLt:t880tfCCtLtGGCGtti1LttfC:tCi1fG0GGG00LftiiGL1LGtitfffLi;1t;;;,,::ftittitLt;:;;tt:,;tf;;iitt;i
11;ttLLfffG81L8Cft1tLCftCf08C00Lt0L180LLitGC0GLGLit1fiffLL11C8CCGf11tti;fCGG0GGGGCCG00GfC0Li:itLf:i1tLtiit1ii1;;if0CC0f1fffi11i;i1tLfiii;:1fiLt:
L;1ii1tfC8LCG1tL10CL00f11tti;;;:1ti1LCGCtfLCtf8CGGff1tLtLC00CLGG0008GLCGGGCCGCCGGCfLLtfCCL1L1:iftLGft1tfLfLfftL1fCftfi;fitCLLfLftLi1t;;;i1::;:i1
;;i1LtC0GCGGL00G0t08fCtfLftf8880Lif81:;18CfGfL1fLtLtttLLLLLLG88000GCCGCGCLfti11i1tfftt1;i1C0C;:11fifC1ifft0CC0fCLLCLG01t11i:ii;;tLf;Lf;1;;t:;ti1
00Lt;CCG0CG@CL8C1CCCG1f1fLL1tGLfGGfLLfftLLGLtf0fL8fttCCLGC888888008808000GGCLft1ttii1;itii1ffLL1itft:;LLft;tt;1tLit8Gf;fGtLG11LCL1itfii1;;ffi1ft
ftLfLfGfCCCCGCi0L.:1LLt11iG@GLCGfLGiC0ttC0LC@@f;ffCtC@GG080000008888888000GC0Cfft111ii;;111fLCLL80LLGGt1LCLtf1;;;t1iifGL,11i1Ctii11ttii;;;:;;111
Lf1Gf1C08GiC81ti,;01;88G80Lti1fLfLfCffGG0CLf1fGCCGGGGLG@8000000000C00CCCCGCLtt1111;:i1LGGCCLLLLLCG00GC08Lfft11t11;itL;.tGfCf1ii1;11tiiit1tf1t;i1
tGCLGGLfGLGCG0GCitLLCC80CL08Gf1Li1fLttLCf;1fLCLGG880G00G00000000000GCGGGCfLftiiiiiitfftfffLLG888GC08880G08Ciitf11f:iffLft1ti1ttt;:tt1fLtiftftLC:
fLLftG000CG00CCfGfLLCCC1L0GGG1it18L;;1Ltitt00GCC888880080008888800000GCLLGCCGLfCCCtfffG880088GGG08@8G0888000Gt;ittLtttii1iLt;;Ltii:;1;1f1;1:ittL
GG00GC00G88CG0@00GiCCfLftttttttft1tLLfLLftL0GGG008880880080G0000G00CGG0880GGG0LLf;:.:iittfCG8@@88000888G088000GLti1CLtftfLtfttftiLLt;LCGtCti111i
80GGCttt11tLLLCCGLLffffft1tf111ii;,,:.   ,f000888000000080880888000GGGGGGCCCCfLLi;;tLLt1LCGGGCCG08@88008@80880008Lttif1:,tftii111ff;1tiiftLCfLfi
tfC0@8GCLft11ii;;;ii;;;;;:;;;;;i;;i;;;;f0LG008000008000000G00G0G0GGGGGCLLCCLtt11;;ti:iLC0GCGG0000GG08@8800888880080f1ifLtf1L111if1i;:Ltf1;ff;:it
Cfi;;;;;:;;;;;;;;;;i;;;;i;;;;;;i;;;ii1tfC088088800008800000G0GG00GGGGLCGf11tti;;,:1fftifCC880G0008800008888088880088GfGC1CffL;tLt1CC1;iiit11ttft
;;;;i;;;;i;ii;;;ii;;;ii;;;i;i;;;;iiii;ifCG808800000000G00G08000GGGGGGCffff1;;;;iii;;ffC0fLGGG0800000808000880888800880LLLLt1L0f11t1tttii1i:1tCLL
;ii;;;ii;;;;;;ii;;ii;;;;i;;ii;iii;i1;;L0008C000800G0008800GGGGGGGGGGCCLLti1i11;;if0CLCCGGG000G088880000888008888880088Ct0fitLLLf1CLLt11i1LLff;;i
;iiiii;;;iiii;;;iiii;ii;;iiiiiiii;1iiGLCG0GG00G000GGGG00880000GCCCGGGCCLt11iii1ttttCGGGC00000000888888000008000088888000ti11fLCfGftfCf1titLt;t1i
iiiiiiiiiii;iiiiiii1iiii11iiiiii11i1GCLL0GGGG00GG88008G00GG0CCGGGCLCCLf1ifCLt11tfLLLLLG00GG00000000888888000000G00888GGLfCtt1iit;:i:1LfGC;:ft:;i
11ii11iii11iii1iii1ii1111i11i1111iiCCLLC08CC0080GGG8GG@80000G0GCCCCLfLLCLf1::itftLCGGGGGG0008888080000888@@0G000G080800CLLfttttf1t111LL1itti111f
111iii1t1ii111ii11i11111tt111tt1fftCC1LG00080000GG8G0000000GGGG00800GCLttfttfLt1fLLLCG000G00GG008888@CC00GC88000GGG000LttiGGCf;:LCt1i:1fti;111ti
tt1111111tt111tt1111t1111tttt1t1tGGLCLC0008808808808000000880000GLCGGCLf11tiitt1;;tLCCCGGG00GGG0GCGGG0GGG880008880000GLfttfLf1LC;1C1;1;tC11tit;i
ftt111tt111ttt1t1tttttttttttttfiLCLCGCG88008888000000000000000880000GGCLLCLLCG8@@8800000000888888@8888888000080888G0GL1itt1;1Ltt1:1Gfff11C80L111
ttfftttttt1111tfttttfftttfftfffff10GLCC00000888880000000000000CG80GG0GGG0CCCLffCGG00GGGG000GG0000888888880080008CLG0GLG0Lt1CL1fft1iiiL8@CfGft11L
tffttfftttftttttfffffffLffffLffCt1GGGGG0880008800000000000000000CG08GCGCftfLCGCfLCCG0080088088088800000000G000GLCG00GCLCii1i1ti;i:t1:;::LLtCGt;L
ffffffttLffffLffffffffffLLLLLLLC1iCGGG8000808800088888000GCCCGCG000GCLLG0LfLffLCLfCGGG0G0088880008008800880GCCG08800fittfLttfGLii1C@C::;:1LCiG0i
ffffffffffLLLfLLLLfLLLLLLLLLLLLLLttfC88888888000GCCCCCLLfLLLCC0CCCG0G00000008GCCG0GGGGG00GG00000008880G0G00LLG800000ft0@fL8LL8GG0LttG8111i:t11t1
fLLfLffLLfffLLLLLLLCCLLCCLLCCCLCCGtfG888888080GCCCLLLLLLLLLffLLLfLLfLCCCCLLG080888800880000000000000G000GGG08000000GGffLifCLG80GCtitCLtffLLti;tt
LLfLLLLLLCLLLLCCCCLCCCCCCCCCCCCGCGCfC080088880GGCCLCCLLLLLLLLffCLCLtfCCCCG8GCCGGG880888888888888880000088888888880080Gt:fGCL1tGGifGLtiLti;ftLL1t
LLLCLLCCCCCCGCLCCCCCCCCCCCCCCGGGGGLtLGGG0888GG0CCLLLfLfffLLLLLLLLLfLfLLffLC000000G0088000008888888808800888G088880t:0G1tfGffG0@G00f1LGLLtLCC0f1f
LLCCCCCCCCGCCCGGCGGCGCGGGCCGGGCGG000CLC@0G@80GGGCLLLLLffffLLLfLLfLLCGCCGCCCGCCGCGCG0000000GG0088888000000888800G0f. :01it:iGf1ff1CLCCL8ftfLf;fLL
CCCCCCCGGGCGGCGGGGGGGGGGGGGGGGGGG008GfLGG000GCLCCCLLLLffLLffffffffffLLLCGCLLCCGGCGGG0000000GGCGG0000000000800000Gt,. ,fLCCLLGfftLGC00;tt;fGfC1,C
CCCCCGGGGGGGGGGGGGGGGGGGGG0GGGGGGG0088tf0000GCCLCCLLLLfLfffffffttffffftttfCGLLLLCGGCG0GG0000GCLCCCGG000GG0008808Lff1itf;tfitLi1GC1LGCffiif80f8L;
CCGGGGGGGGG000GGG0GG0G0G0GGG000G0G00080ft00CCGCLCCCCLCCLLLLLffffffftttt111tttLCCCCCG0000GG0GGGLf11tffLCG00000000G080@@@CC8fii11fLtCffLf1;11LL:LG
GGGGG0GGGG0G000000G00G00GG0G0G0000080008GLGGGCG0CCCGGCCCCLCCCLLfffftttttttttttfLLC0GG0008GGGCCfiii;1ttffLCG0000GGLG88@C::fCfi;tti;1LLfLLLt;f88Gf
GGGG00G000000G0G000000000000000000000G0G80C0LfffLLLLLLLLLLLLLLLLLLLLLt11ttttttt1111tfttttCGG0LLGLi;if11ftfCG000GC0@@81;fCtCGfLftttttLC8CtffG1tiC
0000000000000000000000000000000000000008888GCCCLfttttt11ttt11111111111111t1111111tttttLLLffLftLLLCGL1t11ttLG00CC8@@L;fCt1ftLCCLfLCtfGCtL11ttft1t
00000000000000000000000000000000000000088888Lttftt1i1fLLLCG08GLLf1tttt1111111ttttttL0CtC000GGGGGGGLLLf1;1ffG8008@@CfCfiiitLC11f111fCGf1iLtfLGL;t
0000000000000000000000000000000088888800808@GtfttffCLt1tttffLLLLC0fttttt1tttttffftfCLfffttttt1tfLfLLLftt1tfG000@0i1f;C@GCCfLLftfLttLLtttttftfCtC
880000000000000000000888888888888888888808880ftttttttt1111tttfLLLfffffttttttffffffffLLfft111111tttii111tttfG080titLfC1fffGGff0Cttf1iitLffffL1tCt
L@0000000000880008888088888888888@@0008888008L1ttttt1111111ttttfftfffftttffffffffffttffftt111111ti;;i;:;1tL8@Gt1LtL@tt8G11C1fGCffff1iffLt1111tft
t0800000008888888880888888888@@0GCG8@80G00008G11tt11tt111111ttttttttttftffffffffffttttt11111111t1;ii;;;i1tGGCLf0Ct1tCLftL8CGGfC88t1fLGCf1tfL11LL
;C@8000080008888888888888@@8GCG8@880GG0000888@Li11111ttttttttttttttttttttfffffftftttttttttttttt1iiiiiii11fC0CLC1iffLf1iCL1iLfLGLi00tf00LtfG0CCGG
110888000888888888888@@0GLC8@800GCCCG00888888@0t1111111tttttttttttt1tttttffffftttttttttttttttt11ii111111tC0CC08tt1tffCL;iCftt1CCCLGGfifLtLGCLtG8
G1t@888888888888@@80CCG8@80GCLCCG0G088@@@@@@@@@C111111111111tttttttttttttff1i1ttttttttttttttt111i1111111tG@0GLf0GGCCft1tfitfftiffftfCCGC08tt0GCC
G0fC@888888@@8000080L11ii11fCGGCG0888@G00G0G0088f111111111tt1tttttfLfttttttt1t1ttfLLLftttttt111111111111C80080GttLtt11fftCi1CfC80LC008LtCf1LCftf
0GGG08@@0GGG0Li.,,, i1 ..,,. :CC08880CG88000000@0t11111111111ttttfffffttt;::::itttffffttt11111t1111111iC@8800C1G8LGGLtiC0C0GCfLCLLL08GfLt1LfLGGL
8880GGG0@@@@C; .,,;:,....::::iLCGG0008888080CG8@@G1t111111111tttttttffti;:::::,;tft11ftt1111111111111ti..:tG8CCLLG;t@GftfGGL0C1fGt1tfffLLiitf1iC
0G08@@888i  ,C@1 ,,,,,.,..,;1tCCGG088888800GG000080t11111111tftttt11111i;;;;;;::;1i1tfttt1111111111111,.::,,. ,::::i;ii11tfGCG00Ct111GCCCLCGGCLt
@@800@01 ...;i;G0:,,...,,..,:tGCfCGGG088000000800800f111111ttttffffffftt11111iitffffttttttt11t11111i1f,.::,...:::,..,,,...,,,.  .:i:,,::;;i1CLfC
0G@8i  ,..:,,t: 18i,;..,,....1CGGGGGGGCGGGG0000880GG8C111t1ttfffffLLLLffffffffffLfffffffftttt11111i1Ct ,,..,,;:  :;:,.,;i:,:,.,;,.:i;,. .. :,.iC
@t  .,. ...,,;,  .t:::.::,.,,iGCLCG00GG000GG0800GGGGG8Gt1tttttfft1ttffffLCCCLLLLfffffffftttt111111tCL; ....,;,.,,..,::,,...,;::..,;;, ;ti;iit1:.
 ...,,.,,.,:.,,,. ;;,,.,.,:. ;GGCG00GG000GLCGG800GG00000LttttttfCGCGCLftttfffftttttttfLfttt111111tCC1,,,..::..:,,..,::..... ::...,;..1i;1tf1ifff
.,.,:,,. ..;i.::ii,.;,.,,,,::,fCCCCCGGCGGCLCCLC0800000000CfttttttffLffCGCLLLCGGGGCLLLLffttt1111tfGCLL;..:;,:, .:;1;;:::;,..::.  .:,.;i1::,  ,
.... :;,...,;:.,:ti,,....,,..;CGGGGGGG0GGCCLLLCLC0000000000CfttftttffffffLLLffLffLftttttttt111f00GCCG1 ,:. .ifCL1;:,.,.,, ,:....:: ,i, ,. .,. .:
...,,.;:.,..;;.,,i1;..,.,..  ,LGGCCGCGGGGGCLCLfLCGG0000000080Ltffffffffffffffffftttttttttt11t0800GG0Li:. :tGC;  ...,. ..,:. ,..:;. ;,.. .::. ;:
.......;;..,.t1.,1i.,,,,..,.. :C0GGGGGGGGGGGCCCCLCGCGG00000888GfffffffffffLLfffffffffffttttG880G0000t ,1G8f. .,. .;,:;:,  .. ..;; ,,.:,i1:.,, ..
,..,,:,.;;.,.;1.,:i,.,:,..,  . ;CGGGGGCGGCLCGGCLLfLCCGGGG0088888CfLfLLffLLLLLLLLLLLLffftt0@80000GG1,iL0G, .,,,,..,;;,...,:, .,:i, .,::1;.:;,,:;,
,,,  ;i,.i;,.,t1,,,.,. .:;....,.;GGGGGGGGCCGGGCLLCCCCCCCCGGGG088@8LLLLLLLLLLLLLLLLffftt0@800GGGGLitG@L..,,,,,,...,;,. ,:,...,i;;:..,:i; :i;;,.::
G: ,:..i;.;,:,;f;,;:. .,.......,.10GGGGGCGG000GGCCGGCCCCGGCGCCCCG088CLLLLLLLLfffttffC880GCLCCCLtt08f .,..,...... ,:. .. .....:f:. :;1; :t;, ,,,,
:@L. :,.:;,;,.;t1:,..:;,,,,:,...,.10G0GCGGCCGCGCCGCLCCLCCCLLCGCCGGCC0880000000008880GLLLCCG0GLfG@f  ,...,..,....:;,........,.,;,:.,t1.,t;...:;.,
. G0: .:.:: :i,it:,,;:.,,..,:,,. ..L01LGGGGGGGGGGGCCGGGCCCCCCCGCCCCCLLCCCCCCCLCCLCCGG00GG00CfC8L. ....,,,.....,,:;... ..,....:t;. ;L;.ti,,,:1i.,
.. 18i,.,,,;,:i;:,,,..,:,,:,.,,,,,:. ..,1fCGCCCCCLCCCLCCCCGGGGGCCGGGGGGGGGGGGGGG000000000CLG8G, ..........,...,.:;.....,,...,,:,. if,;1::,:1:.tt
:,, i0i..;;::,;i;,:;:,::,;:,::,,,,.,::;i1LGGCCCCCGGGCGGGGGCGGGCCGGGGGGGCCCGGGGGGG000GGCLCGG8i   ........,,,,:,,,:,..,,,,..,,..;;, :L:i;::::,:ti,
.,,. :Ci. .;;;;ii::,,,,,,....:,  ,ittLCCGGCCGGGCCGGGGGCGGGGGGGG00G0G00000000GG00000CLLG000G, .......,,,,,,,,,,,,::. .,.  ..,..,,, .1ti.tC,.;tt,.
, ,:, ;0;1@Ciii1:::::,..:::;: .1LCCGG000GGGGGG000GGGGGGGGCCCCCGGG000000GGGGGG0GGGCLCGG08f  ...,,,,,.  .,,,,,,.,;:.......... .,:,,:,iLi:f:,i1;,i;
...,.. 10.i@t;11,.,,. ..,,.  iLG8G1:,     ,L0GGCGGGGGGGGG00GGG000GGGGGG000G00GGGCCG88GC: .,,,,...,,,:,  .,:;;;,..,..,,...,..,,,,...;G;:,,1i,:11;
.,:,,;: t8,,8Li:,,,..,,:. .iLG8t  ,,,,,.,.. ,tGGLCGGGGGGGGGGGGGGGGGGCCGGG000GGGCG0f.1t,.......,. .,,.........,,,,,......  .,,,,,.,,:Ct,tt:.1Ct;.
,..,,.,:,L8i:GC1:,...,.. :tC0L,:::,::,,,..,..  iLCGGGGG0GG0GG0GCGGGGCGGG000GLfff11Gf..,,,,.,,....,,,,,:,,,,,.,:,..,,.. .. ...,,.,:,;1,;:,;LL;..,
..,,,,...,f8L,CC:,..... :fG01,,,:,..,,,,..,,,,,. ...:tLCGCCCGGG0GGGGGGCGG00LLLCGC1  ,.,::;i,. .,,...,.,,.,.,,. .:, ,1ti. .. .,,,,i1:,.:;iLL:,,.,
,:;i1ii::,..tCi11;,...,tG801;;;::,,,,,...,,,,...,.,:,,.,ifCG000GGGGGGG0L;f80Lfi,,,,,,,,,;i;;,..  ....,,:;;:.. ...,:.,;1GL, .  .,i1;L8C;:ft;:,...
:,::fGLCGC1: ,;:;:::;tGG0C,,;;;i::;:::,,,::,,,,.,,,..,.,,... .,C8GGGGGGL:.  ,.,....,,,:1i::,:, .......;;ii;i;;:,:,,;,.:.L@L:.,,,:ttC0C,:ti:,.,,,
.:;;.;GCGGG0C; :ti1LGCG0f,:;ii::;:;i;,,::,,,,,,,,,,,.,,,,,,,,,,,;C008C:fC:.......... .11:.,:,     ,,,.,,........, ,:...;,10GLi:;:if00C;f1;f,,:::
,.,;:,.fGGGGGCGC1fGGCG81,;:,,:ii;::::::::::,,,..,..,,,,,:,,;;:ii;,.,  .;GL: .,,.....:11,.,.,,  ,; .:.,, ,,,,,....:,.,:. ,,f8GCi;1CC08Ci11CCGLi;:
:,:,i;:;C00GCC8CtLfCGCi:;:::::;;;;:,,,,.,.,::,::,,::::::::,,.,,,,,,::,..iGf:. .,,,:ifLi;i;;;;itf11tttt1;,,;,:ii;i;;1t1i;.  t8GGt;1C8@G1LGLCLCCGC
:;;,:iLtL8@88@8L1fff1;:;;;::;;iii;;:::;i;;;;;:,,,,,,,:,,..:::;;i;;::,.,,:fGL1::;ii1ft;:,,,:::;;;i1i;:,,,,::,.:;;iiiii11i;::,iCL1;;C0@Ct@GLfCL1;:
1i.:ifCLG88888CffLt1t111:,::::;;:i;:,::;;::,.,:::,,,,:,,,,::,,,,.,:,,,,,:itCfi;;1fft:..,::;:;::;;:,,,,,:::,.:,,;;;;;;i111f1;ifL1if00@GG8CLC1:;i1
.1f,fCL0@888@8f1tff1i11i;:,,,:;iiii:::::::::::::;;:,,::::::;;:;;:,,:,,;i;;1ft111tt1i::,,:::;;;;;;;;;;;::..:::;i;i;:;iii;i11i;itfiiG080G8GCC1ii::
,:LCf8@8888@@Gtttft1ii1;;iiii;,:;:::;;;;;;;,:;::,,:;ii;;:::::;::::::;::,:;1Lf1iitt11i;;;i;;;::::i;;,,::,,,,::,::,:;::,;i::;;;i11t;L880G08L;1i:::
;1fC08888888@L1ft1i;;;iii;;i;;i;:;;;:,:;;;:;;;;;iiii;:;:::;i;;i;11;:;::;ii11tii;;i;,..,:,::;;:::,,:,:,.,,:i1111tf1;;;i;;i1iii1ff1:f808G01ifii1i;
1tC88888888@8t1ttt1ii;ii:i;,.,,:,,,:::;;::;::::::;;::,:i;::,:;:::;iii:,,:;i1ttttt;;;;iii1i;iiiiii1i;:,:,,:::iiit11i;iii1i:;;:;1t1:f@88L1LCftti1i
t8@88888888@Gt1tt1iii;;ii,.,,,,,,,,;:::::,,:,::,,::::;;;i;::;:,,:::;;;:,,:;;i1t1ii:;iiii11i;11i;:::,,,,,:;;:,;iiii;;i;;;:;;;;:,i1;i08LtLLLLLfC1,
800888888@@@C1tt11ii111i;ii;;:,,,,..,,,:::,:;:;1;:::::;:,,;;:;iiii11i;:::::1t11iiit1i1tttt1ti::;;;;:::::;;;i1i;;:,::;;i;:;::i11ii;t08CtLLfLfCfi;
88888@008@80L1tttti;;i111i11;;:,,:;:;;:;;iii;iii;::::,,.,,:;:;;:,,..,,,;;:;it1i;;;;;:;1i;ii;;i;:;,,,:,,::;iii;;1t1;:;:,,:,,,,;i;;:t8GGGCLLffC11i
8800088888G8f11111ii;1ft111ii;;iiiii;i11;:::;::;;;:,:::,,.  ....,,,,,,,,,:;tLf1ii;;i11;i1tii1i;::::,,:;;;iiii1i::;;;;::;i;:;;:;1t;t00GCCC0CfLi11
888888880C80fi;;i1ii1;;i1ttttt1i;;::;;;::::,,,,.................  ....,,....:11;,;;i11ii::;1tf1;:::,:;;11ttii;i;;;;;:::,,::,:::;iiC0GCCGCLftt111
88880008GG8Gtiiii;i;:1t11i:::;i;;;;:,....,,..::..,,,.,,.....,........  ....  .,::,.:;;;;:,,,,....,,,;ii11;;;;;;ii;;iii;::::,,::;:L8GGCfCGftftti1
88888880G88Gfii1i;::;;ii;::;:.,;;:,,,,,:;i;;;;;;i;;:,:,,,,,.,,...,,,,,........,,.,::;;:,,,:,,,:,:;:::;;:ii11i11ii;ii;;;;:,,,,,;;t8GCLLCCGCCC0Li1
808008@GG88GL111iiii;i:::ii;iiii11i111;;::;iii1t1tffttft11t1;:;:,........  .....,,.,:,,,...,,.....,:i11ttttii111iiiiii;:::ii;:::CGGCCLC880ti1ffi
8888800G088GC1tt1iiiiitt1i:;;iitttffffLCCCCCGGGGGGCCGGGGGGGGCGCLLft11i;,.,,. .... .,,,:::::,,,:;itCCLt1;:;;;i111fLftttt11ii;i1;f0GGCCLL808GLff1i
8888880G8880Ctiii;,.,:;tftti;;ii11i111tfttttt1111ttttffLCCCG00GGG0000GLt1i;;;,,..,..,,,..,:i;;itLGGGCCCf1itftitt11tt111iiii111f0GGGCCLG0G0G80tL0

"""
