import sys
sys.path.append('../')
from graph import Cell, Map
import queue

INF = int(1e9)

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

# horizontal & vertical ==> weight = 1
# diagonal ==> weight = 1.5
weight = [1, 1, 1, 1, 1.5, 1.5, 1.5, 1.5]

def heuristic(a, b):
    dx = abs(a.x - b.x)
    dy = abs(a.y - b.y)
    return (dx + dy) - min(dx, dy)

def a_star(s, f, w, h, obs):
    """
    A* algorithm combines Dijkstra and Greedy BFS
    f(x) = g(x) + h(x); g(x) is cost function, h(x) is heuristic function
    """
    # Containers
    path    = [[-1] * w for _ in range(h)]
    cost    = [[INF] * w for _ in range(h)]
    pq      = queue.PriorityQueue()

    # Mark cost at start node as 0
    # Mark previous node at start node as -2
    cost[s.y][s.x] = 0
    path[s.y][s.x] = -2

    # Put start node to priority queue
    # Note: tuple format: (cost, Cell(x, y))
    # f(x) = g(x) + h(x)
    pq.put((heuristic(s, f) + 0, s))

    while not pq.empty():
        u = pq.get()

        # Stop as soon as we reach the end node
        if u[1].x == f.x and u[1].y == f.y:
            break

        # Explore every adjacent nodes
        for i in range(len(dx)):

            # x, y are coordinates of neighbors
            x, y = u[1].x + dx[i], u[1].y + dy[i]

            # Go to the node if it is not a part of obstacles
            if x in range(w) and y in range(h):
                if not obs[y][x]:
                # Update cost at neighbor if possible
                    if (weight[i] + u[0]) < cost[y][x]:
                        cost[y][x] = weight[i] + u[0] 
                        path[y][x] = i
                        priority = cost[y][x] + heuristic(Cell(x, y), f)
                        pq.put((priority, Cell(x, y)))
                    
  # Return (has path, trace path container)
    if cost[f.y][f.x] != INF:
       res = Map.trace_path_by_dir(s, f, path)
       return True, res
    else:
       return False, None
