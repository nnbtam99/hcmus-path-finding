import sys
sys.path.append('../')
from graph import Cell, Map
import queue

INF = int(1e9)

# 4 directions
dx       = [0, 0, 1, -1]
dy       = [1, -1, 0, 0]
weight   = [1, 1, 1, 1]

def dijkstra(s, f, w, h, restricted):

   # Containers
   dirs    = [[-1] * w for _ in range(h)]
   dist    = [[INF] * w for _ in range(h)]
   pq      = queue.PriorityQueue()

   """
   Set 0 as cost of the shortest path from start node to itself
   Set -2 as parent of start node (avoid being mistaken for direction i: 0 - 3)
   """
   dist[s.y][s.x] = 0
   dirs[s.y][s.x] = -2

   """
   Put start node to priority queue
   Note: tuple format: (cost, Cell(x, y))
   """
   pq.put((dist[s.y][s.x], s))

   while not pq.empty():
      u           = pq.get()

      # Stop as soon as we reach the end node
      if u[1].x == f.x and u[1].y == f.y:
         break

      # Explore every adjacent nodes
      for i in range(len(dx)):

         # x, y are coordinates of neighbors
         x, y     = u[1].x + dx[i], u[1].y + dy[i]

         # Go to the node if it is not restricted
         if x in range(w) and y in range(h) and not restricted[y][x]:

            # Update cost at neighbor if possible
            if weight[i] + u[0] < dist[y][x]:
               dist[y][x] = weight[i] + u[0] 
               dirs[y][x] = i
               pq.put((dist[y][x], Cell(x=x, y=y)))              
                                
   has_path    = (dist[f.y][f.x] != INF)
   cost        = -1
   path        = None

   if has_path:
      path     = Map.trace_path_by_dir(s=s, f=f, dirs=dirs)
      cost     = dist[f.y][f.x]

   return has_path, cost, path

def dijkstra_group(s, stops, w, h, obs, dist_s):
   # Containers
   path    = [[-1] * w for _ in range(h)]
   cost    = [[INF] * w for _ in range(h)]
   pq      = queue.PriorityQueue()

   """
   Set 0 as cost of the shortest path from start node to itself
   Set -2 as parent of start node (avoid being mistaken for direction i: 0 - 3)
   """
   cost[s.y][s.x] = 0
   path[s.y][s.x] = -2
   pq.put((cost[s.y][s.x], s))

   while not pq.empty():
      u = pq.get()

      for i in range(len(dx)):
         x, y = u[1].x + dx[i], u[1].y + dy[i]

         if x in range(w) and y in range(h) and not obs[y][x]:
            if (weight[i] + u[0]) < cost[y][x]:
               cost[y][x] = weight[i] + u[0] 
               path[y][x] = i
               pq.put((cost[y][x], Cell(x, y)))

   for stop in stops:
      dist_s[stop] = cost[stop.y][stop.x]

   # Save path and cost of shortest paths
   dist_s['path'] = path
   dist_s['cost'] = cost
