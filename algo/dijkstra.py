import sys
sys.path.append('../')
from graph import Cell
import queue

INF = int(1e9)

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

# horizontal & vertical ==> weight = 1
# diagonal ==> weight = 1.5
weight = [1, 1, 1, 1, 1.5, 1.5, 1.5, 1.5]

def dijkstra(s, f, w, h, obs):

    # Result containers
    path    = [[-1] * w for _ in range(h)]
    cost    = [[INF] * w for _ in range(h)]
    pq      = queue.PriorityQueue()

    # Mark cost at start node as 0
    # Mark previous node at start node as -2
    cost[s.y][s.x] = 0
    path[s.y][s.x] = -2

    # Put start node to priority queue
    # Note: tuple format: (cost, Cell(x, y))
    pq.put((cost[s.y][s.x], s))

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
                        pq.put((cost[y][x], Cell(x, y)))
                                
                                
    # Return (has path, trace path container)
    if cost[f.y][f.x] != INF:
       return True, path
    else:
       return False, None
