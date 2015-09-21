graph = {(1,1): [(1,2), (2,1),],
         (1,2): [(1,3), (2,2)],
         (2,1): [(2,2),(3,1)],
         (2,2): [(2,3),(3,2)],
        (3,2): [(4,2)],
        (2,3): [(2,4),(3,3)]}

def find_path(graph, start, end, path=[]):
        path = path + [start]
        print path
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            print 
            if node not in path:
                newpath = find_path(graph, node, end, path)
                print newpath
                if newpath:
                    print newpath
                    return newpath
        return None
    
#A sample run (using the graph above):
#    >>> find_path(graph, 'A', 'D')
#    ['A', 'B', 'C', 'D']
#    >>> 

find_path(graph, (1,1), (3,3))
