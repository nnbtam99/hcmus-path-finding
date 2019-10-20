import sys
sys.path.append('../')
from graph import Cell, Map
import queue

INF = int(1e9)

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
weight = [1, 1, 1, 1]

"""
A* algorithm combines Dijkstra and Greedy BFS
f(x) = g(x) + h(x); g(x) is cost function, h(x) is heuristic function
"""
def a_star(s, f, w, h, restricted):

    def heuristic(a, b):
        dx, dy    = abs(a.x - b.x), abs(a.y - b.y)
        return (dx + dy) - min(dx, dy)

    # Containers
    dirs    = [[-1] * w for _ in range(h)]
    dist    = [[INF] * w for _ in range(h)]
    pq      = queue.PriorityQueue()
   
    """
    Put start node to priority queue
    Note: tuple format: (cost, Cell(x, y))
    f(x) = g(x) + h(x)
    """
    pq.put((heuristic(s, f) + 0, s)) 
    dist[s.y][s.x]   = 0
    dirs[s.y][s.x]   = -2

    while not pq.empty():
        u            = pq.get()
        ux, uy       = u[1].x, u[1].y

        # Stop as soon as we reached the end node
        if ux == f.x and uy == f.y:
            break

        # Explore every adjacent nodes
        for i in range(len(dx)):

            # x, y are coordinates of neighbors
            x, y     = ux + dx[i], uy + dy[i]

            # Go to the node if it is not restricted
            if x in range(w) and y in range(h) and not restricted[y][x]:

                # Update cost at neighbor if possible
                if weight[i] + u[0] < dist[y][x]:
                     dist[y][x]  = weight[i] + u[0]
                     dirs[y][x]  = i
                     priority    = dist[y][x] + heuristic(Cell(x=x, y=y), f)
                     pq.put((priority, Cell(x=x, y=y)))


    has_path      = (dist[f.y][f.x] != INF)
    cost          = -1
    path          = None

    if has_path:
        path      = Map.trace_path_by_dir(s=s, f=f, dirs=dirs)
        cost      = dist[f.y][f.x]

    return has_path, cost, path
