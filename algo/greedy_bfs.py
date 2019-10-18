import sys
sys.path.append('../')
from graph import Cell
import queue

# 8 directions
dx = [0, 0, 1, -1, 1, 1, -1, -1]
dy = [1, -1, 0, 0, 1, -1, 1, -1]

def heuristic(a, b):
    # On a square grid that allows 8 directions of movement
    # Use diagonal distance
    dx = abs(a.x - b.x)
    dy = abs(a.y - b.y)
    return (dx + dy) - min(dx, dy)

def greedy_bfs(s, f, w, h, obs):

    '''
    Greedy BFS algorithm uses heuristic function instead of cost.
    h(x) --> heuristic function
    '''

    # Result containers
    visited  = [[False] * w for _ in range(h)]
    path    = [[-1] * w for _ in range(h)]
    pq      = queue.PriorityQueue()

    # Mark cost at start node as 0
    # Mark previous node at start node as -2
    path[s.y][s.x] = -2

    # Put start node to priority queue
    # Note: tuple format: (cost, Cell(x, y))
    pq.put((heuristic(s, f), s))

    while not pq.empty():
        u = pq.get()

        # Stop as soon as we reach the end node
        if u[1].x == f.x and u[1].y == f.y:
            break

        # Explore every adjacent nodes
        for i in range(len(dx)):

            # x, y are coordinates of neighbors
            x, y = u[1].x + dx[i], u[1].y + dy[i]

            if x in range(w) and y in range(h) and not visited[y][x]:
                visited[y][x] = True
                
                # Go to the node if it is not a part of obstacles
                if not obs[y][x]:
                    path[y][x] = i
                    priority = heuristic(Cell(x, y), f)
                    pq.put((priority, Cell(x, y)))
                    
  # Return (has path, trace path container)
    if visited[f.y][f.x]:
       return True, path
    else:
       return False, None




    