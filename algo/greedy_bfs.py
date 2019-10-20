import sys
sys.path.append('../')
from graph import Cell, Map
import queue

# 4 directions
dx       = [0, 0, 1, -1]
dy       = [1, -1, 0, 0]
weight   = [1, 1, 1, 1]


def greedy_bfs(s, f, w, h, restricted):
    """
    Greedy BFS algorithm uses heuristic function instead of cost.
    h(x) --> heuristic function
    """
    def heuristic(a, b):
        dx, dy  = abs(a.x - b.x), abs(a.y - b.y)
        return (dx + dy) - min(dx, dy)

    # Containers
    visited    = [[False] * w for _ in range(h)]
    dist       = [[-1] * w for _ in range(h)]
    dirs       = [[-1] * w for _ in range(h)]
    pq         = queue.PriorityQueue()

    visited[s.y][s.x]   = True
    dirs[s.y][s.x]      = -2
    dist[s.y][s.x]      = 0

    """
    Put start node to priority queue
    Note: tuple format: (cost, Cell(x, y))
    """
    pq.put((heuristic(s, f), s))

    while not pq.empty():
        u         = pq.get()
        ux, uy    = u[1].x, u[1].y

        # Stop as soon as we reached end node
        if ux == f.x and uy == f.y:
            break

        # Explore every adjacent nodes
        for i in range(len(dx)):

            # x, y are coordinates of neighbors
            x, y  = ux + dx[i], uy + dy[i]

            if x in range(w) and y in range(h) and not visited[y][x]:
                visited[y][x] = True
                
                # Go to the node if it is not restricted
                if not restricted[y][x]:
                    dirs[y][x]   = i
                    dist[y][x]   = weight[i] + dist[uy][ux]
                    priority     = heuristic(Cell(x=x, y=y), f)
                    pq.put((priority, Cell(x=x, y=y)))
           
    cost    = -1
    path    = None
         
    if visited[f.y][f.x]:
       path    = Map.trace_path_by_dir(s=s, f=f, dirs=dirs)
       cost    = dist[f.y][f.x]
       
    return visited[f.y][f.x], cost, path
